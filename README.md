# 📄 AI Invoice & Document Extractor

Ein automatisierter Python-Workflow zur Extraktion strukturierter Rechnungsdaten aus PDF-Dokumenten mithilfe von Large Language Models (OpenAI API / LLMs). Die extrahierten Daten werden validiert, in eine Excel-Tabelle exportiert und die verarbeiteten Dateien strukturiert archiviert.

---

## 🚀 Features

* **Automatisierter Ordner-Workflow:** Überwachung des Eingangspfads (`/inbox`) auf neue PDF-Rechnungen.
* **PDF-Textextraktion:** Effizientes Auslesen unstrukturierter Dokumenteninhalte.
* **LLM-basierte Extraktion:** Strukturierte Umwandlung in JSON via OpenAI API (Rechnungsnummer, Datum, Brutto-/Nettobeträge, USt., Empfänger/Aussteller).
* **Excel-Generierung & Export:** Automatisches Anlegen bzw. Aktualisieren einer Excel-Tabelle (`invoices.xlsx`) mit allen extrahierten Rechnungsdaten.
* **Dateiverwaltung & Archivierung:** Automatisches Verschieben und standardisiertes Umbenennen verarbeiteter Dokumente nach `/processed`.

---

## 📁 Projekt- & Ordnerstruktur

Stelle sicher, dass im Hauptverzeichnis des Projekts folgende Ordner existieren:

```text
├── inbox/            # Hier werden neue, unverarbeitete PDF-Rechnungen abgelegt
├── processed/        # Hierhin werden verarbeitete PDFs automatisch verschoben
├── .env              # Enthält deinen OPENAI_API_KEY (nicht auf GitHub pushen)
├── main.py           # Hauptskript
├── requirements.txt  # Python-Abhängigkeiten
└── invoices.xlsx     # Automatisch erstellte Excel-Tabelle mit allen extrahierten Daten