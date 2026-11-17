---
name: genpark-doc-processor
description: Intelligent document, PDF, and spreadsheet data extractor.
version: 1.0.0
---

# genpark-doc-processor

## MCP runtime requirements

The standard-library-only policy applies to direct `client.py` use. Running `mcp_server.py` requires Python 3.10+ and the official `mcp` SDK (`mcp>=1.0.0,<2`) from `requirements.txt`. Install it into your chosen environment from the repository checkout:

```bash
python -m pip install -r requirements.txt
```

Configure the MCP client with that environment's absolute Python executable path and the absolute path to `mcp_server.py`. The client launches a local STDIO process; a GitHub URL is not a remote MCP endpoint.

## Overview
This skill mitigates the "messy data" problem. It takes unstructured or poorly formatted documents, PDFs, or raw data feeds and outputs clean, structured tables, summaries, or presentation outlines.

## Capabilities
1. **Data Structuring**: Turn messy conversational data or raw text dumps into clean CSV/Markdown tables.
2. **Report Summarization**: Take long business reports and extract only action items, financial figures, and core arguments.
3. **Presentation Generation**: Draft complete slide-by-slide outlines for business presentations based on raw notes.

## Usage Instructions
When a user provides raw data or asks to process a document:
- First, clarify the desired output format (Table, JSON, Slide Outline).
- Strip out all irrelevant fluff and directly address the structured data output.
- If data is ambiguous, create a "Needs Clarification" column or section in the output.
