# FinRecon AI

AI-powered financial reconciliation and exception analysis prototype.

## Problem
Finance teams spend significant time reconciling bank transactions against general-ledger records and investigating exceptions.

## Solution
FinRecon AI combines deterministic Python/SQL reconciliation logic with GenAI-powered explanation of exceptions.

### Features
- Bank vs. general-ledger reconciliation
- Match, mismatch, missing and duplicate detection
- Exception-value and vendor analysis
- Interactive Streamlit dashboard
- Optional OpenAI-powered exception analysis
- Finance-focused natural-language summaries

## Architecture
User → Streamlit → Reconciliation Engine → Bank + Ledger Data
                         ↓
                  Exception Analysis
                         ↓
                    GenAI Assistant

## Tech Stack
Python, Pandas, SQL/SQLite, Streamlit, OpenAI API, REST APIs

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

For AI analysis, set `OPENAI_API_KEY` as an environment variable.

## Design principle
Financial calculations and reconciliation classifications are deterministic. The LLM is used for explanation and summarization rather than calculating financial values.
