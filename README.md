
# Veritas Clean Scraper

Veritas Clean Scraper is an enterprise-grade, compliance-first data ingestion pipeline. It is designed to extract unstructured text from public web nodes, validate data quality boundaries, scrub personal information automatically, and format the output for direct use in Large Language Model (LLM) training and Retrieval-Augmented Generation (RAG) systems.

## Key Engineering Features

- **Automated Compliance Check**: Automatically requests, downloads, and processes a target site's `robots.txt` configuration rules. It instantly blocks tasks that hit forbidden paths.
- **Politeness Throttling**: Implements a randomized delay window between 2.0 and 4.5 seconds to protect target server infrastructure from request overload.
- **Asynchronous Execution Architecture**: Powered by Python's `asyncio` and `Playwright` to run background web browser sessions efficiently without halting host memory.
- **Anti-Bot Shielding**: Normalizes the automated browser's screen dimensions and identity fingerprints to replicate a standard, modern desktop layout.
- **Layout Adaptation Engine**: Uses text-density calculations to isolate the core reading content on a webpage, ignoring menus, headers, footers, and code fragments even if website HTML class tags change.
- **Pydantic Quality Gate & GDPR Scrubbing**: Filters out short or corrupted records under a 50-character threshold. It scans text payloads using regular expressions to replace emails and phone numbers with protected tags automatically.
- **LangChain RAG Handshake**: Prepares data for AI ingestion using a recursive splitter that slices documents into overlapping 500-character fragments, optimizing them for vector storage.

## Project Structure

```text
veritas-clean-scraper/
│
├── config/
│   └── targets.json         # Targeting configurations and rules
│
├── core/
│   ├── __init__.py
│   ├── ai_ingestion.py      # Local file storage and LangChain chunking logic
│   ├── compliance.py        # Robots.txt parser and throttling delays
│   ├── extraction_engine.py # Playwright automation and text density algorithm
│   └── validation_gateway.py# Pydantic templates and PII sanitization filters
│
├── data/
│   └── certified_training_data.json # Structurally validated JSON output
│
└── run.py                   # Central pipeline orchestration root
```

## How It Works (Example Pipeline Log Flow)

1. The `TargetQueueManager` reads ingestion nodes from the configuration file.
2. The `EthicalComplianceGate` checks the remote host rules and applies a politeness pause.
3. The `AsynchronousExtractor` boots a virtual browser tab, downloads the layout, and filters out non-content areas.
4. The `DataValidationGateway` runs strict property checks and scrubs sensitive text.
5. The `AIIngestionStorage` writes a clean JSON array to disk and passes text fragments to the LangChain token processors.

