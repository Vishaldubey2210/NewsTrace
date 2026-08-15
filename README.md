<div align="center">

<br/>

<img src="https://img.shields.io/badge/NewsTrace-Autonomous%20Media%20Intelligence-6c63ff?style=for-the-badge&logo=rss&logoColor=white" alt="NewsTrace Banner"/>

<br/><br/>

# 🗞️ NewsTrace

### *Autonomous Media Intelligence System*

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask&logoColor=white"/>
  <img src="https://img.shields.io/badge/spaCy-NLP-09A3D5?style=flat-square&logo=spacy&logoColor=white"/>
  <img src="https://img.shields.io/badge/Playwright-Scraping-2EAD33?style=flat-square&logo=playwright&logoColor=white"/>
  <img src="https://img.shields.io/badge/NetworkX-Graph_Analysis-orange?style=flat-square"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square"/>
  <img src="https://img.shields.io/badge/Hack_of_Thrones-2025-purple?style=flat-square"/>
</p>

<p align="center">
  <b>Profile journalists autonomously · Zero LLMs · Built for Hack of Thrones 2025</b>
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-tech-stack">Tech Stack</a> •
  <a href="#-screenshots">Screenshots</a> •
  <a href="#-how-it-works">How It Works</a> •
  <a href="#-api-reference">API Reference</a>
</p>

</div>

---

## 🎯 What is NewsTrace?

**NewsTrace** is a fully autonomous journalist profiling system that scrapes, analyzes, and visualizes journalist data from any news outlet — **without using a single LLM or paid API**.

Just enter a news outlet name and let the system:
- 🔍 Find the outlet's official website automatically
- 🕷️ Scrape journalist profiles intelligently
- 🧠 Analyze text using spaCy & NLTK (no LLM cost!)
- 📊 Build interactive journalist-topic network graphs
- 💾 Export complete journalist data as CSV or JSON

> Built for **Hack of Thrones 2025** — autonomously profiling media at scale.

---

## ✨ Features

<table>
<tr>
<td width="50%">

#### 🤖 Autonomous Website Detection
Multi-algorithm search that finds official news outlet websites from just a name — no manual URL needed.

#### 🕸️ Playwright + BeautifulSoup Hybrid Scraper
Adapts to any site structure — handles JavaScript-heavy pages and static HTML alike.

#### 🧠 NLP Analysis (Zero LLMs)
spaCy entity extraction + NLTK keyword analysis + TextBlob sentiment — all local, all free.

</td>
<td width="50%">

#### 📊 Interactive Network Graphs
Vis.js powered journalist-topic relationship maps with real-time physics simulation.

#### 🎯 Influence Scoring Engine
Custom PageRank-inspired algorithm that ranks journalists by cross-topic reach and impact.

#### 📁 Export & REST API
Download complete journalist datasets as CSV or query via a clean REST API with 21 endpoints.

</td>
</tr>
</table>

---

## 🖼️ Screenshots

### 🏠 Landing Page — Autonomous Media Intelligence

![Landing Page](https://raw.githubusercontent.com/Vishaldubey2210/NewsTrace/main/Screenshot%20(369).png)

---

### 🔧 Core Features & Tech Stack Overview

![Features Page](https://raw.githubusercontent.com/Vishaldubey2210/NewsTrace/main/Screenshot%20(370).png)

---

### 📊 Dashboard — Real-Time Analytics Hub

![Dashboard](https://raw.githubusercontent.com/Vishaldubey2210/NewsTrace/main/Screenshot%20(372).png)

---

### 🔍 Search — Profile Any News Outlet

![Search Page](https://raw.githubusercontent.com/Vishaldubey2210/NewsTrace/main/Screenshot%20(374).png)

---

### 🕸️ Network Graph Visualization

![Network Graph](https://raw.githubusercontent.com/Vishaldubey2210/NewsTrace/main/Screenshot%20(375).png)

---

### 📈 Advanced Analytics Dashboard

![Analytics](https://raw.githubusercontent.com/Vishaldubey2210/NewsTrace/main/Screenshot%20(377).png)

---

## 🚀 Quick Start

### Prerequisites

```
Python 3.9+   pip   2GB free space
```

### Installation (5 Minutes)

```bash
# 1. Clone the repository
git clone https://github.com/Vishaldubey2210/NewsTrace.git
cd NewsTrace

# 2. Create & activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download NLP model
python -m spacy download en_core_web_sm

# 5. Install Playwright browser drivers
python -m playwright install chromium

# 6. Create environment config
cp .env.example .env

# 7. Launch the app!
python -X utf8 run.py
```

### ✅ Access the Application

Open your browser: **http://localhost:5000**

That's it! 🎉

---

## 💻 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | Python 3.9+ · Flask 3.0 | Core web framework & API |
| **Scraping** | Playwright · BeautifulSoup4 · lxml | Intelligent web scraping |
| **NLP** | spaCy 3.x · NLTK · TextBlob | Entity extraction, sentiment, keywords |
| **Graph Analysis** | NetworkX · python-louvain | Journalist relationship networks |
| **Search** | DuckDuckGo Search API | Autonomous outlet discovery |
| **Database** | SQLite · SQLAlchemy | Persistent journalist data storage |
| **Frontend** | Bootstrap 5 · jQuery · Vis.js · Chart.js | Rich, interactive UI |
| **ML (Optional)** | scikit-learn | TF-IDF keyword extraction, LDA topics |

---

## ⚙️ How It Works

```
┌─────────────────────────────────────────────────────────┐
│                   NewsTrace Pipeline                    │
└─────────────────────────────────────────────────────────┘

 1. INPUT       → User enters a news outlet name
                      ↓
 2. DISCOVER    → Multi-source search finds official website URL
                      ↓
 3. SCRAPE      → Playwright + BS4 extracts journalist profiles
                      ↓
 4. NLP         → spaCy / NLTK analyzes bios, topics, entities
                      ↓
 5. SCORE       → PageRank-inspired influence scoring
                      ↓
 6. GRAPH       → NetworkX builds journalist-topic network
                      ↓
 7. VISUALIZE   → Vis.js renders interactive graph in browser
                      ↓
 8. EXPORT      → CSV / JSON download or REST API access
```

---

## 📖 Usage Guide

### 1️⃣ Profile a News Outlet

1. Navigate to the **Search** page
2. Enter any outlet name (e.g., `The Hindu`, `BBC`, `Reuters`)
3. Click **"Start Autonomous Profiling"**
4. Wait 2–5 minutes while the AI agents work
5. View results on the Dashboard!

**What you get back:**
| Data | Example |
|------|---------|
| Journalist Name | Priya Sharma |
| Bio / Description | Senior Political Correspondent |
| Beats / Topics | Politics, Economy, National |
| Contact Info | email, Twitter handle |
| Profile URL | Direct link to journalist page |
| Influence Score | 87.4 / 100 |

### 2️⃣ Explore the Network Graph

1. Go to **Network** page
2. Select an outlet from the dropdown
3. Interact with the graph:
   - 🖱️ **Click** nodes to see journalist details
   - 🖱️ **Drag** to reposition nodes
   - 🔍 **Search** to highlight specific journalists
   - 📤 **Export** the graph as JSON

### 3️⃣ Advanced Analytics

1. Navigate to **Analytics** page
2. View beat distribution charts, influence score histograms
3. Filter by outlet, beat, or date range
4. Export charts or raw data

---

## 🌐 API Reference

Base URL: `http://localhost:5000/api`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | System health check |
| `GET` | `/outlets` | List all profiled outlets |
| `POST` | `/scrape` | Start a new profiling job |
| `GET` | `/journalists` | Get all journalists |
| `GET` | `/journalists/<id>` | Get journalist by ID |
| `GET` | `/network/<outlet>` | Get network graph data |
| `GET` | `/analytics/summary` | Overall analytics summary |
| `GET` | `/export/csv` | Export data as CSV |
| `GET` | `/export/json` | Export data as JSON |

### Example Request

```bash
# Start profiling a news outlet
curl -X POST http://localhost:5000/api/scrape \
  -H "Content-Type: application/json" \
  -d '{"outlet_name": "The Hindu"}'

# Check API health
curl http://localhost:5000/api/health
```

### Example Response

```json
{
  "service": "NewsTrace API",
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-08-16T03:22:00Z"
}
```

---

## 📁 Project Structure

```
NewsTrace/
├── 📂 app/
│   ├── 📂 agents/          # Autonomous scraping agents
│   ├── 📂 database/        # SQLite models & queries
│   ├── 📂 nlp/             # spaCy, NLTK, TextBlob modules
│   ├── 📂 analytics/       # Influence scoring & analytics
│   ├── 📂 graph/           # NetworkX graph builders
│   └── routes.py           # All 21 Flask API routes
├── 📂 frontend/            # HTML templates + static assets
│   ├── templates/
│   └── static/
├── 📂 data/
│   ├── database/           # SQLite database files
│   └── exports/            # CSV & JSON exports
├── 📂 scripts/             # Utility scripts
├── 📂 tests/               # Unit tests (pytest)
├── config.py               # App configuration
├── run.py                  # Entry point
├── requirements.txt        # Python dependencies
└── .env.example            # Environment template
```

---

## 🔧 Configuration

Copy `.env.example` to `.env` and configure:

```env
# Flask
FLASK_ENV=development
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
SECRET_KEY=your-secret-key-here

# Database
DATABASE_PATH=data/database/newstrace.db

# Scraping
SCRAPING_DELAY=2
MAX_RETRIES=3
RESPECT_ROBOTS_TXT=True

# NLP
SPACY_MODEL=en_core_web_sm
ENABLE_SENTIMENT_ANALYSIS=True

# Export
EXPORT_PATH=data/exports/
```

---

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific test file
pytest tests/test_scraper.py -v
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. **Fork** the repository
2. Create your feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m 'Add AmazingFeature'`
4. Push to the branch: `git push origin feature/AmazingFeature`
5. Open a **Pull Request**

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🏆 Acknowledgements

- Built for **Hack of Thrones 2025** hackathon
- Powered by [spaCy](https://spacy.io/), [Playwright](https://playwright.dev/python/), [NetworkX](https://networkx.org/), [Vis.js](https://visjs.org/)
- Zero LLMs used — pure NLP + classical ML

---

<div align="center">

**Made with ❤️ by [Vishal Dubey](https://github.com/Vishaldubey2210)**

<br/>

⭐ **Star this repo if you found it useful!** ⭐

<br/>

<img src="https://img.shields.io/github/stars/Vishaldubey2210/NewsTrace?style=social"/>
<img src="https://img.shields.io/github/forks/Vishaldubey2210/NewsTrace?style=social"/>

</div>
