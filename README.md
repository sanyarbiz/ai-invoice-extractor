# 📄 AI Invoice & Document Extractor

Ein automatisierter Python-Workflow zur Extraktion strukturierter Rechnungsdaten aus PDF-Dokumenten mithilfe von Large Language Models (OpenAI API / LLMs). Die extrahierten Daten werden validiert, in Excel exportiert und die Originaldateien standardisiert archiviert.

---

## 🚀 Features

* **Automatisiertes Dateimonitoring:** Überwachung eines Eingangsordners auf neue PDF-Rechnungen.
* **PDF-Textextraktion:** Effizientes Auslesen unstrukturierter Dokumenteninhalte.
* **LLM-basierte Extraktion:** Strukturierte Umwandlung in JSON via OpenAI API (Rechnungsnummer, Datum, Brutto-/Nettobeträge, USt., Empfänger/Aussteller).
* **Excel-Export:** Automatisches Schreiben und Anhängen der Datensätze an eine Excel-Tabelle.
* **Dateiverwaltung:** Saubere, standardisierte Umbenennung und Archivierung verarbeiteter Dokumente.

---

## 🛠️ Tech Stack

* **Sprache:** Python 3.10+
* **KI & LLM:** OpenAI API (`gpt-4o-mini` / `gpt-3.5-turbo`) oder lokale LLMs (z. B. via Ollama)
* **Libraries:** `openai`, `pypdf` / `pdfplumber`, `pandas`, `openpyxl`, `python-dotenv`

---

## ⚙️ Installation & Setup

### 1. Repository klonen
```bash
git clone [https://github.com/DEIN-BENUTZERNAME/ai-invoice-extractor.git](https://github.com/DEIN-BENUTZERNAME/ai-invoice-extractor.git)
cd ai-invoice-extractor