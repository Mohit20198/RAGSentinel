<div align="center">

# RAGSentinel

**Enterprise Agentic RAG · LangGraph · Gemini Embeddings · NeMo Guardrails · Qdrant**

[![CI](https://github.com/Mohit20198/RAGSentinel/actions/workflows/ci.yml/badge.svg)](https://github.com/Mohit20198/RAGSentinel/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agentic-green)](https://github.com/langchain-ai/langgraph)
[![Qdrant](https://img.shields.io/badge/Vector%20DB-Qdrant-red)](https://qdrant.tech)

> A production-grade, enterprise agentic RAG system that separates **technical signal** from **noisy data** using LangGraph cyclic reasoning, semantic reranking, conversation memory, and NeMo Guardrails for safety.

</div>

---

## What is RAGSentinel?

RAGSentinel is built around a core insight: **not all retrieved documents are equal**. Most RAG systems treat all retrieved content the same — RAGSentinel uses a multi-stage intelligence pipeline to:

- 🛡️ **Guard** every query through NeMo Guardrails before retrieval even begins
- 🧠 **Plan** whether to retrieve or respond from memory using conversation history
- 🔍 **Retrieve** from a Qdrant vector store using 3072-dim Gemini embeddings
- 📊 **Rerank** results locally with FlashRank for zero-latency semantic scoring
- ✅ **Respond** with grounded, traceable answers via Groq Llama 3.3 70B

---

## Agent Flow

```
User Query
    │
    ▼
┌─────────────────┐
│ NeMo Guardrails │  ◄── blocks jailbreaks, off-topic, injections
└────────┬────────┘
         │ Pass
         ▼
┌─────────────────┐
│  Planner Node   │  ◄── routes: CONVERSATIONAL vs TECHNICAL
└────────┬────────┘
         │
    ┌────┴─────┐
    │          │
    ▼          ▼
Responder   Retriever Node
 (memory)       │
            FlashRank Reranker
                │
            Responder Node
                │
            ◄── LangGraph MemorySaver (thread memory)
```

---

## Architecture

```
ragsentinel/
├── app/
│   ├── agents/
│   │   ├── nodes/
│   │   │   ├── planner.py      # Routes: conversational vs technical
│   │   │   ├── retriever.py    # Embeds query → Qdrant search → FlashRank
│   │   │   └── responder.py    # Synthesizes final answer with Groq LLM
│   │   ├── graph.py            # LangGraph state machine definition
│   │   └── state.py            # AgentState TypedDict schema
│   ├── gateway/
│   │   └── client.py           # Portkey LLM gateway (primary + fallback Groq)
│   ├── guardrails/
│   │   └── rails.py            # NeMo Guardrails — input/output safety filter
│   ├── ingestion/
│   │   ├── chunking/
│   │   │   └── splitter.py     # Paragraph-based splitter (1500 char max)
│   │   └── loaders/
│   │       ├── pdf.py          # pypdf + pdfplumber local PDF parsing
│   │       ├── html.py         # BeautifulSoup HTML extraction
│   │       ├── office.py       # python-docx / python-pptx parsing
│   │       └── text.py         # Plain text loader
│   ├── services/retrieval/
│   │   ├── embedding.py        # Gemini text-embedding-2-preview (3072-dim)
│   │   ├── qdrant_service.py   # Qdrant Cloud vector search
│   │   └── ranking_service.py  # FlashRank local cross-encoder reranking
│   ├── config.py               # Centralised env var management
│   └── main.py                 # FastAPI entrypoint — /query, /health, /graph
├── ui/
│   └── app.py                  # Streamlit chat UI with reasoning step display
├── evals/
│   ├── pipeline.py             # RAGAS evaluation runner (6 metrics)
│   └── app.py                  # Streamlit 3-tab eval dashboard
├── tests/
│   └── test_health.py          # pytest health + root endpoint checks
├── .github/workflows/ci.yml    # GitHub Actions — lint, format, type-check, test
├── docker-compose.yml          # Orchestrates backend + UI containers
├── Makefile                    # Developer shortcuts
├── pyproject.toml              # Ruff, Mypy, Pytest config
└── requirements.txt            # All dependencies (prod + dev)
```

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Orchestration** | LangGraph + LangChain | Cyclic agent state machine with memory |
| **LLM** | Groq Llama 3.3 70B via Portkey | Fast inference with automatic fallback |
| **Guardrails** | NVIDIA NeMo Guardrails | Input/output safety and topic filtering |
| **Vector DB** | Qdrant Cloud | High-performance ANN vector search |
| **Embeddings** | Gemini `gemini-embedding-2-preview` | 3072-dim semantic text embeddings |
| **Reranking** | FlashRank (local) | Zero-latency cross-encoder reranking |
| **Document Parsing** | pypdf, pdfplumber, BS4, python-docx | Local parsing — no external OCR |
| **Observability** | Pydantic Logfire + LangSmith | Full distributed tracing across every node |
| **Evaluation** | RAGAS + DeepEval | 6-metric RAG quality assessment suite |
| **API** | FastAPI + Uvicorn | Async REST API with Swagger UI |
| **Frontend** | Streamlit | Chat UI with reasoning transparency |
| **CI/CD** | GitHub Actions | Automated lint, test, type-check on push |
| **Containerisation** | Docker + Docker Compose | One-command local orchestration |

---

## Quick Start

### Prerequisites

- Python 3.10+
- A Qdrant Cloud account (free tier works)
- API keys for: Groq, Portkey, Gemini, LangSmith, Logfire

### 1. Clone and install

```bash
git clone https://github.com/Mohit20198/RAGSentinel.git
cd RAGSentinel
make install
```

### 2. Configure environment

Copy and fill in your API keys:

```bash
cp .env.example .env
```

```env
# LLM (Groq via Portkey)
GROQ_API_KEY=""
GROQ_FALLBACK_API_KEY=""
PORTKEY_API_KEY=""

# Vector DB
QDRANT_API_KEY=""
QDRANT_CLUSTER_ENDPOINT=""     # e.g. https://your-cluster.cloud.qdrant.io:6333

# Gemini Embeddings
GEMINI_API_KEY=""

# Observability
LOGFIRE_TOKEN=""
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=""
LANGSMITH_PROJECT=""

# Eval judge (separate key to avoid rate-limiting live app)
JUDGE_GROQ=""

# Streamlit → FastAPI
BACKEND_URL=""                 # e.g. http://localhost:8000
```

### 3. Ingest documents

Drop your files (PDF, DOCX, HTML, PPTX, TXT) into `DATA/` and run:

```bash
python -m app.ingestion.processor DATA --wipe
```

> `--wipe` drops and recreates the Qdrant collection. Omit to append.

### 4. Run the application

**Option A — Docker Compose (recommended):**
```bash
make docker-up
# Backend → http://localhost:8000
# UI      → http://localhost:8501
```

**Option B — Local processes:**
```bash
# Terminal 1
make run-backend     # FastAPI on :8000

# Terminal 2
make run-ui          # Streamlit on :8501
```

### 5. Run the eval suite (optional)

```bash
# Requires the backend running on :8000
streamlit run evals/app.py
```

---

## Developer Commands

```bash
make install      # Install all dependencies
make format       # Auto-format code with Ruff
make lint         # Lint check with Ruff
make typecheck    # Static type analysis with Mypy
make test         # Run pytest suite
make docker-up    # Start all services via Docker Compose
make docker-down  # Stop Docker Compose services
make clean        # Remove all __pycache__ and build artifacts
```

---

## Documentation Index

| # | Guide | What it covers |
|---|---|---|
| 01 | [System Overview](DOCS/01_SYSTEM_OVERVIEW.md) | End-to-end architecture and design decisions |
| 02 | [Ingestion Engine](DOCS/02_INGESTION_ENGINE.md) | Document parsing and Qdrant indexing pipeline |
| 03 | [Node Intelligence](DOCS/03_NODE_INTELLIGENCE.md) | Planner, Retriever, Responder internals |
| 04 | [Observability](DOCS/04_TRACING_AND_OBSERVABILITY.md) | Logfire + LangSmith distributed tracing |
| 05 | [Environment Variables](DOCS/05_ENVIRONMENT_VARIABLES.md) | Full configuration reference |
| 06 | [Known Gotchas](DOCS/06_KNOWN_GOTCHAS.md) | Non-obvious bugs and architectural decisions |
| 07 | [FlashRank Reranking](DOCS/07_FLASHRANK_RERANKING.md) | Local semantic reranker deep-dive |
| 08 | [Guardrails](DOCS/08_GUARDRAILS.md) | NeMo Guardrails implementation guide |
| 09 | [LLM Gateway](DOCS/09_LLM_GATEWAY.md) | Portkey routing, fallback, and observability |
| 10 | [Evals](DOCS/10_EVALS.md) | RAGAS metrics theory and token budget |
| 11 | [Evals Pipeline](DOCS/11_EVALS_PIPELINE.md) | Live eval pipeline and Streamlit demo |

---

## Evaluation Metrics (RAGAS)

RAGSentinel ships with a 6-metric RAGAS evaluation suite:

| Metric | Measures |
|---|---|
| **Faithfulness** | Is the answer grounded in the retrieved context? |
| **Answer Relevancy** | Does the answer address the question asked? |
| **Context Precision** | Are the retrieved chunks actually relevant? |
| **Context Recall** | Are all necessary facts present in context? |
| **Answer Correctness** | Is the answer factually correct? |
| **Tool Correctness** | Custom Jaccard-based retrieval accuracy |

---

## CI / CD

Every push to `main` automatically runs:

1. **Ruff** — format check + lint
2. **Mypy** — static type analysis
3. **Pytest** — endpoint health tests

View the latest run → [GitHub Actions](https://github.com/Mohit20198/RAGSentinel/actions)

---

## License

Distributed under the [MIT License](LICENSE).

---

<div align="center">
  <sub>Built for high-scale enterprise document intelligence.</sub>
</div>
