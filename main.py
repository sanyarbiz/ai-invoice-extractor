import os
import shutil
from pathlib import Path
from dotenv import load_dotenv
import pdfplumber
import pandas as pd
from pydantic import BaseModel, Field
from openai import OpenAI

# Umgebungsvariable & Client laden
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Schema definieren mit Pydantic
class InvoiceData(BaseModel):
    invoice_number: str = Field(description="Rechnungsnummer/Belegnummer")
    recipient: str = Field(description="Rechungsempfänger/Kunde")
    vendor: str = Field(description="Rechungssteller/Unternehmen")#
    gross_amount: float = Field(description="Gesamtbetrag/Bruttobetrag")
    tax_amount: float = Field(description="Umsatzsteuer/MwSt. Betrag")
    invoice_date: str = Field(description="Rechungsdatum YYYY-MM-DD")

# PDF-Text extrahieren
def extract_text_from_pdf(pdf_path: Path) -> str:
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
    return full_text

# KI-Extraktion mit OpenAI Structured Outputs
def parse_invoice_with_ai(text: str) -> InvoiceData:
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Du bist ein präziser Buchhaltungs-Assistent. Extrahiere alle relevanten Daten aus der Rechnung."
            },
            {"role": "user", "content": text},
        ],
        response_format=InvoiceData,
    )
    return completion.choices[0].message.parsed

# Daten an Excel-Tabelle anhängen
def append_to_excel(data: InvoiceData, excel_file: Path):
    df_new = pd.DataFrame([data.model_dump()])

    if excel_file.exists():
        df_existing = pd.read_excel(excel_file, engine="openpyxl")
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new

    df_combined.to_excel(excel_file, index=False, engine="openpyxl")

# Haupt code
def process_invoices():
    base_dir = Path(__file__).parent
    inbox_dir = base_dir / "inbox"
    processed_dir = base_dir / "processed"
    excel_path = base_dir / "rechnungen.xlsx"

    inbox_dir.mkdir(exist_ok=True)
    processed_dir.mkdir(exist_ok=True)

    pdf_files = list(inbox_dir.glob("*.pdf"))
    if not pdf_files:
        print("Keine neuen PDFs im inbox-Ordner gefunden")
        return

    for pdf_path in pdf_files:
        print("\nProcessing PDF: ", pdf_path)

        # 1. Text holen
        raw_text = extract_text_from_pdf(pdf_path)
        if not raw_text.strip():
            print(f"Warnung: Kein Text in {pdf_path.name} gefunden. Evtl. ein Bild bzw. Scan und kein Text?")
            continue

        # 2. KI befragen
        parsed_data = parse_invoice_with_ai(raw_text)
        print(f"Extrahiert: {parsed_data.vendor} | {parsed_data.invoice_number} | {parsed_data.gross_amount}€")

        # 3. In Excel eintragen
        append_to_excel(parsed_data, excel_path)

        # 4. Datei sauber umbenennen und verschieben
        # Format: YYYY-MM-DD_Vendor_Rechnungsnr.pdf
        clean_vendor = "".join(c for c in parsed_data.vendor if c.isalnum() or c in (' ', '_', '-')).strip()
        clean_inv_num = "".join(c for c in parsed_data.invoice_number if c.isalnum() or c in ('-', '_')).strip()
        new_filename = f"{parsed_data.invoice_date}_{clean_vendor}_{clean_inv_num}.pdf"

        target_path = processed_dir / new_filename
        shutil.move(str(pdf_path), str(target_path))
        print(f"Verschoben nach: {target_path.name}")

if __name__ == "__main__":
    process_invoices()