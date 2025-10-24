

## 📄 **README.md - CRISP & AESTHETIC VERSION**

```markdown
<div align="center">

# 🗞️ NewsTrace

**Autonomous Media Intelligence System**

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-green?style=flat-square&logo=flask)
![spaCy](https://img.shields.io/badge/NLP-spaCy-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

*Profile journalists autonomously • No LLMs needed • Built for Hack of Thrones 2025*

[Features](#-features) • [Quick Start](#-quick-start) • [Tech Stack](#-tech-stack) • [Demo](#-demo)

</div>

---

## 🎯 What is NewsTrace?

**NewsTrace** automatically profiles journalists from any news outlet using AI agents, web scraping, and NLP - all **without using any LLMs**. Just enter an outlet name, and watch the magic happen!

### The Problem
Tracking journalist profiles, beats, and influence across news outlets is time-consuming and requires expensive LLM APIs.

### Our Solution
A fully autonomous system that:
- 🔍 Finds outlet websites automatically
- 🕷️ Scrapes journalist profiles intelligently  
- 🧠 Analyzes text using spaCy (no LLMs!)
- 📊 Builds relationship networks
- 💾 Exports complete data

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🤖 Autonomous Detection
Auto-discovers official websites from outlet names using multi-search algorithms

### 🕸️ Smart Scraping
Playwright + BeautifulSoup hybrid that adapts to any site structure

### 🧠 NLP Analysis
spaCy & NLTK for entity extraction, keyword analysis - zero LLMs!

</td>
<td width="50%">

### 📊 Network Graphs
Interactive Vis.js visualizations of journalist-topic relationships

### 🎯 Influence Scoring
Custom PageRank algorithm ranks journalist influence

### 📁 Export Ready
Download profiles as CSV or access via REST API

</td>
</tr>
</table>

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- pip
- 2GB free space

### Installation (5 minutes)

```
# 1. Clone repository
git clone https://github.com/yourusername/NewsTrace.git
cd NewsTrace

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Download NLP model
python -m spacy download en_core_web_sm

# 6. Install browsers
playwright install

# 7. Create config file
echo "FLASK_ENV=development
FLASK_HOST=0.0.0.0
FLASK_PORT=5000" > .env

# 8. Run!
python run.py
```

### Access the App

Open browser: **http://localhost:5000**

That's it! 🎉

---

## 💻 Tech Stack

<table>
<tr>
<td align="center" width="20%">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="50"/>
<br><b>Python</b>
</td>
<td align="center" width="20%">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flask/flask-original.svg" width="50"/>
<br><b>Flask</b>
</td>
<td align="center" width="20%">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sqlite/sqlite-original.svg" width="50"/>
<br><b>SQLite</b>
</td>
<td align="center" width="20%">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/bootstrap/bootstrap-original.svg" width="50"/>
<br><b>Bootstrap</b>
</td>
<td align="center" width="20%">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg" width="50"/>
<br><b>JavaScript</b>
</td>
</tr>
</table>

**Backend:** Flask • spaCy • NLTK • NetworkX • Playwright • BeautifulSoup  
**Frontend:** Bootstrap 5 • jQuery • Chart.js • Vis.js  
**Database:** SQLite • SQLAlchemy

---

## 🎨 Screenshots

<div align="center">

### Landing Page
![Landing](https://via.placeholder.com/800x400/667eea/ffffff?text=Beautiful+Gradient+Landing+Page)

### Dashboard
![Dashboard](https://via.placeholder.com/800x400/764ba2/ffffff?text=Real-Time+Analytics+Dashboard)

### Network Graph
![Network](https://via.placeholder.com/800x400/f093fb/ffffff?text=Interactive+Network+Visualization)

</div>

---

## 📖 How to Use

### 1️⃣ Profile an Outlet

```
1. Go to Search page
2. Enter outlet name: "The Hindu"
3. Click "Start Autonomous Profiling"
4. Wait 2-5 minutes
5. View results!
```

**What you get:**
- ✅ Journalist names & bios
- ✅ Beats/topics covered
- ✅ Contact info (email, Twitter)
- ✅ Influence scores
- ✅ Profile URLs

### 2️⃣ Explore Network Graph

```
1. Go to Network page
2. Select outlet from dropdown
3. Interact with graph:
   - Click nodes for details
   - Drag to rearrange
   - Zoom to explore
```

### 3️⃣ View Analytics

```
1. Go to Dashboard
2. See live stats
3. Track scraping jobs
4. Monitor system health
```

### 4️⃣ Export Data

```
Click "Export CSV" on results page
OR
Use API: GET /api/export/csv/{outlet_id}
```

---

## 🔌 API Endpoints

```
# Health check
GET /api/health

# Start profiling
POST /api/profile
{
  "outlet_name": "The Hindu"
}

# Get journalists
GET /api/journalists/{outlet_id}

# Get network graph
GET /api/network/graph/{outlet_id}

# Export CSV
GET /api/export/csv/{outlet_id}

# Recent jobs
GET /api/jobs/recent
```

---

## 📁 Project Structure

```
NewsTrace/
├── run.py                 # Entry point
├── config.py             # Configuration
├── requirements.txt      # Dependencies
├── app/
│   ├── __init__.py      # Flask factory
│   ├── routes.py        # API routes
│   ├── models.py        # Database models
│   ├── agents/          # Multi-agent system
│   ├── scrapers/        # Web scraping
│   ├── database/        # DB & graphs
│   ├── nlp/             # NLP processing
│   └── utils/           # Helpers
├── frontend/
│   ├── static/          # CSS, JS, Images
│   └── templates/       # HTML pages
├── data/                # Auto-generated
│   ├── database/       # SQLite files
│   ├── cache/          # Cached data
│   └── exports/        # CSV exports
└── logs/                # Application logs
```

---

## 🔧 Configuration

Create `.env` file:

```
# Flask
FLASK_ENV=development
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# Scraping
SCRAPING_DELAY=3
MAX_PROFILES_PER_OUTLET=50
MIN_PROFILES_REQUIRED=30

# Features
ENABLE_CACHING=True
PLAYWRIGHT_HEADLESS=True
```

---

## 🐛 Troubleshooting

### Module not found?
```
# Activate virtual environment first!
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### Port already in use?
```
# Change port in .env
FLASK_PORT=5001
```

### Playwright error?
```
playwright install
```

### spaCy model missing?
```
python -m spacy download en_core_web_sm
```

---

## 🎯 Key Features Explained

### 🤖 Autonomous Detection
```
Input: "The Hindu"
    ↓
Search Engine Query
    ↓
URL Validation & Scoring
    ↓
Output: https://thehindu.com
```

### 🕷️ Smart Scraping
```
Dynamic content? → Playwright
Static HTML?     → BeautifulSoup
Adapts automatically!
```

### 🧠 NLP Pipeline
```
Raw Text
    ↓
spaCy → Entity Extraction
    ↓
NLTK  → Keyword Analysis
    ↓
LDA   → Topic Modeling
    ↓
Result: Beat Classification
```

### 📊 Influence Score
```
Score = 0.4 × Articles
      + 0.3 × Topic Diversity
      + 0.2 × Recency
      + 0.1 × Cross-Outlet Bonus
```

---

## 🚀 Deployment

### Local Development
```
python run.py
```

### Production (Gunicorn)
```
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Docker (Coming Soon)
```
docker build -t newstrace .
docker run -p 5000:5000 newstrace
```

---

## 🤝 Contributing

```
# Fork → Clone → Branch → Commit → Push → PR
git checkout -b feature/amazing-feature
git commit -m "Add amazing feature"
git push origin feature/amazing-feature
```

---

## 📄 License

MIT License - feel free to use for your projects!

---

## 👥 Team

**Team kur-kure Coders**  
Built for **Hack of Thrones 2025** 🏆

---

## 🙏 Acknowledgments

- **spaCy** - NLP magic
- **Playwright** - Reliable scraping
- **NetworkX** - Graph algorithms
- **Flask** - Elegant web framework

---

<div align="center">

### ⭐ Star this repo if you like it!

**Made with ❤️ for transparent journalism**

[⬆ Back to Top](#-newstrace)

</div>
```

***

## ✅ **WHAT'S DIFFERENT:**

### ✂️ **Removed:**
- Excessive details
- Long explanations
- Redundant sections

### ✨ **Added:**
- Clean badges
- Visual table layouts
- Quick 5-minute setup
- Short feature descriptions
- Icons & emojis
- Centered headings
- Clear structure

### 🎯 **Key Sections:**
1. **What is it** - 2 lines
2. **Features** - Table format
3. **Quick Start** - 8 commands
4. **Tech Stack** - Visual icons
5. **Usage** - 4 simple steps
6. **API** - Quick reference
7. **Troubleshooting** - Common issues

***
