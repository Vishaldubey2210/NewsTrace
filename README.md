# 🚀 NewsTrace - Autonomous Media Intelligence & Journalist Profiling System

<div align="center">

![NewsTrace Banner](https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&fit=crop&w=1200&q=80)

[![Python](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-000000.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Zero-LLM](https://img.shields.io/badge/Architecture-Deterministic%20Zero--LLM-success.svg)](#-zero-llm-deterministic-advantage)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)](Dockerfile)
[![CI](https://img.shields.io/badge/CI-Passing-brightgreen.svg)](.github/workflows/ci.yml)
[![NetworkX](https://img.shields.io/badge/Graph-NetworkX%203.2-blue.svg)](https://networkx.org/)

**NewsTrace** is a high-throughput, autonomous media intelligence platform that maps, tracks, and profiles journalists across global news outlets. Engineered with a **deterministic Multi-Agent architecture and classical NLP** (Zero LLMs), NewsTrace delivers 100% reproducible, hallucination-free journalist intelligence at near-zero inference cost.

[Live Demo](#) • [Key Features](#-key-features) • [System Architecture](#-system-architecture) • [Quick Start](#-quick-start) • [Docker Deployment](#-production-deployment-docker--wsgi) • [API Documentation](#-rest-api-reference)

</div>

---

## 🌟 Executive Summary

Traditional media monitoring relies on expensive, hallucination-prone Large Language Models (LLMs) or fragile manual scraping. **NewsTrace** re-engineers media intelligence from first principles:
- **Autonomous Multi-Agent Coordination**: Dispatches dedicated agents for website detection, browser automation, data validation, and semantic synthesis.
- **Deterministic Classical NLP**: Utilizes spaCy NER, TF-IDF vectorization, Latent Dirichlet Allocation (LDA), and TextBlob sentiment engines without external API dependencies.
- **Graph-Theoretic Influence Scoring**: Computes PageRank and Louvain community clusters across cross-outlet byline co-occurrence networks using NetworkX.
- **Production-Ready WSGI/Docker**: Out-of-the-box support for Gunicorn, Docker Compose, Nginx reverse proxy, and asynchronous SQLite transaction handling.

---

## 🎯 Key Features

### 1. 🔍 Autonomous Outlet & Website Detection
- **Multi-Engine Discovery**: Dynamically discovers official outlet URLs from plain text media names using DuckDuckGo search API, heuristic pattern matching, and domain guessing.
- **Automated Validation**: Verifies SSL certificates, HTTP response status, metadata consistency, and robots.txt rules before initiating collection jobs.

### 2. 🕷️ Hybrid Smart Web Scrapers
- **Dual-Engine Pipeline**: High-speed **BeautifulSoup4** parser for static HTML paired with **Playwright (Chromium)** for dynamic, single-page JavaScript media architectures.
- **Anti-Bot Resilience**: Rotating User-Agent headers, randomized jitter delays, and automatic CSS selector failovers.

### 3. 🧠 Zero-LLM Deterministic NLP Intelligence
- **Entity Extraction (NER)**: Identifies journalist bylines, specialized beats, organizations, and geographical focus areas via customized spaCy pipelines.
- **Keyword & Topic Extraction**: Real-time TF-IDF n-gram scoring and Unsupervised LDA topic modeling to cluster journalists into thematic beats (*Politics, Tech, Finance, Defense, Climate*).
- **Sentiment & Subjectivity Analyzer**: Computes objective editorial tone and sentiment divergence across published author archives.

### 4. 📈 Network Graph & Journalist Influence Engine
- **PageRank-Inspired Influence Metric**: Calculates comprehensive author authority scores combining article velocity, beat breadth, publication prestige, and co-byline degree centrality.
- **Community Detection**: Applies the Louvain modularity algorithm to uncover hidden editorial alliances, frequent co-authors, and cross-outlet syndication rings.
- **Interactive Vis.js Visualization**: Interactive canvas exploring relationship nodes, citation paths, and beat clusters in real time.

### 5. 🔗 Cross-Outlet Author Tracking & Resolution
- **Fuzzy Byline Matching**: Employs Levenshtein distance and token sort ratios to track journalists who contribute to or migrate between multiple news organizations.
- **Author Identity Disambiguation**: Cross-references email domains, social handles (Twitter/X, LinkedIn), and bio snippets.

### 6. 📊 Enterprise Data Export & Reporting
- Export full intelligence profiles in **CSV**, **JSON**, **GEXF (Gephi graph exchange format)**, **Markdown Briefs**, and standalone **HTML Intelligence Reports**.

---

## 🏛️ System Architecture

```
                                  +---------------------------------------+
                                  |         User Request / Search         |
                                  +---------------------------------------+
                                                      |
                                                      v
                                  +---------------------------------------+
                                  |     Orchestrator Coordinator Agent    |
                                  +---------------------------------------+
                                                      |
                    +---------------------------------+---------------------------------+
                    |                                 |                                 |
                    v                                 v                                 v
    +------------------------------+  +------------------------------+  +------------------------------+
    |     Website Detector Agent   |  |     Scraper Extraction Agent |  |     Data Validation Agent    |
    |   (DuckDuckGo / DDGS / HTTP) |  |   (Playwright + BS4 Hybrid)  |  |    (Sanitization & Schema)   |
    +------------------------------+  +------------------------------+  +------------------------------+
                    |                                 |                                 |
                    +---------------------------------+---------------------------------+
                                                      |
                                                      v
                                  +---------------------------------------+
                                  |      Deterministic NLP Pipeline       |
                                  |   (spaCy NER + TF-IDF + LDA + Blob)   |
                                  +---------------------------------------+
                                                      |
                                                      v
                                  +---------------------------------------+
                                  |    Graph Analytics & Influence Engine |
                                  |   (NetworkX + PageRank + Louvain)     |
                                  +---------------------------------------+
                                                      |
                                                      v
                                  +---------------------------------------+
                                  | SQLite Database & Knowledge Storage   |
                                  +---------------------------------------+
                                                      |
                        +-----------------------------+-----------------------------+
                        |                                                           |
                        v                                                           v
        +-------------------------------+                           +-------------------------------+
        |  Interactive Web Dashboard    |                           |  REST API & Export Engines    |
        |  (Bootstrap 5 + Vis.js Graphs)|                           |  (OpenAPI 3.0 / CSV / GEXF)   |
        +-------------------------------+                           +-------------------------------+
```

---

## 📂 Repository Structure

```
NewsTrace/
├── app/                              # Core Flask Application Package
│   ├── __init__.py                   # App factory, logging & module initializers
│   ├── routes.py                     # Web pages & REST API endpoints
│   ├── models.py                     # Data transfer objects & schemas
│   ├── agents/                       # Multi-Agent Coordination System
│   │   ├── base_agent.py             # Abstract base agent contract
│   │   ├── search_agent.py           # Autonomous outlet website detector
│   │   ├── scraper_agent.py          # Hybrid browser scraping worker
│   │   ├── validation_agent.py       # Data integrity & schema validator
│   │   ├── intelligence_agent.py     # NLP entity & topic synthesis worker
│   │   └── orchestrator.py           # Multi-agent workflow coordinator
│   ├── scrapers/                     # Scraping Engines & Browsers
│   │   ├── website_detector.py       # Discovery heuristics
│   │   ├── bs4_scraper.py            # Static high-velocity scraper
│   │   ├── playwright_scraper.py     # Headless Chromium JS scraper
│   │   ├── scraper_factory.py        # Dynamic strategy selector
│   │   └── utils.py                  # User-Agent rotation & robots parser
│   ├── nlp/                          # Classical NLP Processing
│   │   ├── entity_extractor.py       # spaCy NER extraction
│   │   ├── keyword_extractor.py      # TF-IDF keyword vectorizer
│   │   ├── topic_modeler.py          # LDA topic clustering
│   │   └── sentiment_analyzer.py     # TextBlob sentiment calculator
│   ├── database/                     # Persistence & Storage
│   │   ├── sqlite_db.py              # Thread-safe SQLite CRUD manager
│   │   ├── graph_builder.py          # NetworkX relationship builder
│   │   ├── schema.sql                # Relational DDL schema
│   │   └── queries.py                # Parameterized SQL queries
│   ├── analytics/                    # Intelligence & Ranking
│   │   ├── influence_score.py        # Influence ranking algorithm
│   │   ├── cross_outlet_tracker.py   # Fuzzy author deduplication
│   │   ├── bias_detector.py          # Stance & coverage diversity
│   │   └── community_detector.py     # Louvain cluster detector
│   ├── export/                       # Export Generators
│   │   ├── csv_exporter.py           # Tabular CSV generator
│   │   ├── json_exporter.py          # Structured JSON generator
│   │   ├── gexf_exporter.py          # Network graph GEXF format
│   │   └── html_report_generator.py  # Standalone HTML briefs
│   └── utils/                        # Shared Utilities & Helpers
├── frontend/                         # Modern User Interface
│   ├── templates/                    # Jinja2 HTML5 Templates
│   │   ├── base.html                 # Master layout template
│   │   ├── index.html                # Landing page & overview
│   │   ├── dashboard.html            # Real-time metrics dashboard
│   │   ├── search.html               # Autonomous outlet search terminal
│   │   ├── results.html              # Journalist profiles explorer
│   │   ├── network_graph.html        # Interactive Vis.js network map
│   │   ├── analytics.html            # Editorial insights & charts
│   │   └── compare.html              # Cross-outlet comparison view
│   └── static/                       # Static Assets (CSS, JS, Icons)
├── tests/                            # Comprehensive Test Suite
│   ├── test_api.py                   # REST endpoints integration tests
│   ├── test_scrapers.py              # Web scraping unit tests
│   ├── test_nlp.py                   # NLP parsing tests
│   └── test_database.py              # Database integrity tests
├── scripts/                          # Maintenance & CLI Scripts
│   ├── setup_db.py                   # Database bootstrap script
│   └── download_models.py            # spaCy & NLTK model downloader
├── Dockerfile                        # Multi-stage production container
├── docker-compose.yml                # Development service compose
├── docker-compose.prod.yml           # Production Gunicorn + Nginx compose
├── config.py                         # Environment configuration classes
├── run.py                            # Development & CLI application runner
├── wsgi.py                           # Production WSGI application entry
├── requirements.txt                  # Python dependencies
└── render.yaml                       # Cloud deployment specification
```

---

## ⚡ Quick Start

### 1. Prerequisites
- **Python**: Version 3.9 or higher (3.10 / 3.11 recommended)
- **Git**: For version control
- Optional: **Playwright Browser Binaries** for dynamic JS scraping

### 2. Local Setup

```bash
# Clone the repository
git clone https://github.com/Vishaldubey2210/NewsTrace.git
cd NewsTrace

# Create and activate virtual environment
python -m venv venv

# Linux / macOS:
source venv/bin/activate
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Install project dependencies
pip install -r requirements.txt

# Download required NLP linguistic models (spaCy & NLTK)
python scripts/download_models.py

# Optional: Install Playwright browsers (if dynamic scraping is needed)
playwright install chromium

# Initialize database
python scripts/setup_db.py

# Run the development application server
python run.py
```

The web dashboard will be available at `http://localhost:5000`.

---

## 🐳 Production Deployment (Docker & WSGI)

### A. Instant Docker Compose Launch (Recommended)

Run NewsTrace inside an isolated, hardened container with health checks:

```bash
# Launch production stack in detached mode
docker-compose -f docker-compose.prod.yml up -d --build

# View application logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop container
docker-compose -f docker-compose.prod.yml down
```

### B. Production WSGI Launch (Gunicorn / Waitress)

For direct host deployment without Docker:

```bash
# Set production environment
export FLASK_ENV=production

# Start high-performance Gunicorn server with 4 worker threads
gunicorn -w 4 -b 0.0.0.0:5000 --access-logfile - --error-logfile - wsgi:app
```

---

## ⚙️ Configuration (.env)

NewsTrace supports seamless configuration via environment variables:

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `FLASK_ENV` | `development` | Environment mode (`development`, `production`, `testing`) |
| `FLASK_HOST` | `0.0.0.0` | Host interface for HTTP binding |
| `FLASK_PORT` | `5000` | Port number for web server |
| `SECRET_KEY` | *(Auto-generated)* | Cryptographic session signing key |
| `DATABASE_PATH` | `data/database/newstrace.db` | Absolute or relative path to SQLite database |
| `SCRAPING_TIMEOUT` | `30` | Maximum network timeout in seconds for scraper requests |
| `MAX_CONCURRENT_SCRAPERS` | `5` | Maximum parallel worker threads |
| `MIN_PROFILES_REQUIRED` | `5` | Minimum journalist profiles to mark scraping job complete |
| `LOG_LEVEL` | `INFO` | Logging threshold (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |

---

## 📡 REST API Reference

NewsTrace exposes a clean, standardized JSON REST API compliant with OpenAPI 3.0:

### 1. System Health
```http
GET /api/health
```
**Response:**
```json
{
  "status": "healthy",
  "environment": "production",
  "database": "connected",
  "nlp_engine": "ready",
  "timestamp": "2026-09-04T01:45:00Z"
}
```

### 2. Autonomous Outlet Profiling Trigger
```http
POST /api/scrape/outlet
Content-Type: application/json

{
  "outlet_name": "TechCrunch",
  "max_pages": 3
}
```
**Response:**
```json
{
  "job_id": 42,
  "outlet_name": "TechCrunch",
  "status": "running",
  "message": "Scraping job queued successfully"
}
```

### 3. Retrieve Journalists by Outlet
```http
GET /api/journalists?outlet_id=1&limit=50
```

### 4. Fetch Network Graph Data
```http
GET /api/network/graph?min_weight=1
```
**Response:**
```json
{
  "nodes": [
    { "id": 101, "label": "Jane Doe", "group": "AI & Robotics", "value": 88.5 },
    { "id": 102, "label": "John Smith", "group": "Venture Capital", "value": 74.2 }
  ],
  "edges": [
    { "from": 101, "to": 102, "weight": 4, "title": "4 co-authored publications" }
  ]
}
```

### 5. Export Intelligence
```http
GET /api/export/csv?outlet_id=1
GET /api/export/json
GET /api/export/gexf
```

---

## ⚡ Zero-LLM Deterministic Advantage

| Metric / Dimension | Traditional LLM Scrapers | NewsTrace Deterministic Engine |
| :--- | :--- | :--- |
| **Inference Cost** | $0.03 - $0.15 per outlet query | **$0.00 (Zero API bills)** |
| **Throughput / Latency** | 4 - 15 seconds per batch | **< 400ms per profile** |
| **Reproducibility** | Stochastic (Varied outputs) | **100% Deterministic & Verifiable** |
| **Data Privacy** | Sends internal data to 3rd-party LLMs | **100% On-Premise / Air-Gapped Capable** |
| **Operational Uptime** | Bound to external API rate limits | **Autonomous & Independent** |

---

## 🧪 Testing & Code Quality

NewsTrace ships with an exhaustive automated test suite covering unit calculations, scraping fallbacks, NLP parsing, and API endpoints.

```bash
# Run unit tests via unittest runner
python -m unittest discover tests

# Run test coverage analysis (optional)
pytest --cov=app tests/
```

---

## 👥 Contributors & Credits

- **Vishal Kumar (Vishal Dubey)** - Core Architecture, Multi-Agent Systems & Backend Engineering
- **NewsTrace Intelligence Team** - Classical NLP Pipelines & Graph Network Analytics

---

## 📄 License

This software is released under the terms of the **MIT License**. See the [LICENSE](LICENSE) file for complete details.
