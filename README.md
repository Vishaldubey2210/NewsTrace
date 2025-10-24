

## 📄 **README.md - ULTRA DETAILED VERSION**

**Location:** `NewsTrace_full/README.md`

```markdown
# 🗞️ NewsTrace - Autonomous Media Intelligence System

<div align="center">

![NewsTrace Banner](https://via.placeholder.com/1200x300/667eea/ffffff?text=NewsTrace+-+Autonomous+Media+Intelligence)

**An autonomous, scalable, and LLM-free system for profiling journalists from news outlets**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Hack of Thrones 2025](https://img.shields.io/badge/Hackathon-Hack%20of%20Thrones%202025-purple.svg)](https://hackofthrones.com)

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [API Docs](#-api-documentation) • [Architecture](#-architecture)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Screenshots](#-screenshots)
- [Tech Stack](#-tech-stack)
- [System Architecture](#-system-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
  - [Windows](#windows)
  - [Linux/Mac](#linuxmac)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [Usage Guide](#-usage-guide)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Features Breakdown](#-features-breakdown)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [Team](#-team)
- [Acknowledgments](#-acknowledgments)

---

## 🌟 Overview

**NewsTrace** is a fully autonomous media intelligence system designed to profile journalists from news outlets **without using any Large Language Models (LLMs)**. Built for **Hack of Thrones 2025**, this system demonstrates that powerful AI applications can be created using traditional NLP, graph algorithms, and smart scraping techniques.

### 🎯 Problem Statement

Tracking journalist profiles, their beats, influence, and cross-outlet connections is crucial for:
- **Media monitoring agencies**
- **PR professionals**
- **Researchers studying journalism**
- **News organizations** tracking competition

**Challenge:** Most existing solutions require manual data entry or expensive LLM APIs.

**Our Solution:** A fully autonomous system that:
1. Takes an outlet name as input
2. Automatically finds its website
3. Scrapes journalist profiles
4. Analyzes their topics/beats
5. Calculates influence scores
6. Builds relationship networks
7. Tracks journalists across outlets

**ALL WITHOUT A SINGLE LLM CALL!** ✨

---

## 🚀 Features

### Core Capabilities

#### ✅ 1. Autonomous Website Detection
- **Multi-Search Algorithm:** DuckDuckGo + fallback strategies
- **Smart URL Validation:** Verifies official domains
- **Pattern Recognition:** Identifies common news outlet URL patterns
- **Confidence Scoring:** Ranks potential URLs by likelihood

#### ✅ 2. Intelligent Web Scraping
- **Dual-Mode Scraper:**
  - **Playwright** for dynamic JavaScript-heavy sites
  - **BeautifulSoup** for static HTML parsing
- **Adaptive Strategy:** Switches between modes based on content
- **User-Agent Rotation:** Mimics real browser behavior
- **Retry Mechanism:** 3 attempts with exponential backoff
- **Respect Robots.txt:** Ethical scraping practices

#### ✅ 3. NLP-Powered Analysis
- **Named Entity Recognition:** spaCy for person/organization extraction
- **Keyword Extraction:** NLTK-based TF-IDF analysis
- **Topic Modeling:** LDA (Latent Dirichlet Allocation)
- **Beat Classification:** Categories like Politics, Sports, Tech, etc.
- **No LLMs Required:** Pure algorithmic NLP

#### ✅ 4. Network Analysis
- **Graph Construction:** NetworkX for relationship graphs
- **Journalist-Topic Edges:** Connects people to their beats
- **Influence Scoring:** Custom PageRank-style algorithm
- **Cross-Outlet Tracking:** Fuzzy matching to identify same journalists
- **Interactive Visualization:** Vis.js powered network graphs

#### ✅ 5. Beautiful Dashboard
- **Real-Time Monitoring:** Live stats and job tracking
- **Gradient UI:** Eye-catching modern design
- **Responsive Layout:** Works on desktop, tablet, mobile
- **Dark Theme:** Easy on the eyes
- **Interactive Charts:** Chart.js and Plotly visualizations

#### ✅ 6. Export & Integration
- **CSV Export:** Download complete profiles
- **JSON API:** RESTful endpoints for integration
- **Batch Processing:** Handle multiple outlets
- **Scheduled Jobs:** (Coming soon) Automated updates

---

## 📸 Screenshots

### Landing Page
![Landing Page](docs/screenshots/landing.png)

### Dashboard
![Dashboard](docs/screenshots/dashboard.png)

### Network Graph
![Network Graph](docs/screenshots/network.png)

### Search & Profiling
![Search](docs/screenshots/search.png)

### Analytics
![Analytics](docs/screenshots/analytics.png)

---

## 🛠️ Tech Stack

### Backend

| Technology | Version | Purpose |
|-----------|---------|---------|
| **Python** | 3.9+ | Core language |
| **Flask** | 3.0.0 | Web framework |
| **SQLite** | 3.x | Database |
| **SQLAlchemy** | 2.0.23 | ORM |
| **Playwright** | 1.40.0 | Dynamic scraping |
| **BeautifulSoup4** | 4.12.2 | HTML parsing |
| **spaCy** | 3.7.2 | NLP processing |
| **NLTK** | 3.8.1 | Text analysis |
| **NetworkX** | 3.2.1 | Graph algorithms |
| **Pandas** | 2.1.4 | Data manipulation |
| **NumPy** | 1.26.2 | Numerical computing |

### Frontend

| Technology | Version | Purpose |
|-----------|---------|---------|
| **Bootstrap** | 5.3.2 | UI framework |
| **jQuery** | 3.7.1 | DOM manipulation |
| **Chart.js** | 4.4.0 | Data visualization |
| **Plotly.js** | 2.27.0 | Advanced charts |
| **Vis.js** | 9.1.2 | Network graphs |
| **Font Awesome** | 6.5.1 | Icons |
| **Google Fonts** | - | Typography |

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    FLASK APPLICATION                     │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Routes     │  │    Models    │  │   Config     │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
├─────────────────────────────────────────────────────────┤
│                   MULTI-AGENT SYSTEM                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │Website Agent │  │Profile Agent │  │  NLP Agent   │ │
│  │  Detection   │  │  Extraction  │  │  Analysis    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
├─────────────────────────────────────────────────────────┤
│                    DATA PROCESSING                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Scrapers   │  │  Database    │  │ Graph        │ │
│  │ Playwright   │  │  SQLite      │  │ Builder      │ │
│  │    + BS4     │  │              │  │ NetworkX     │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
├─────────────────────────────────────────────────────────┤
│                      FRONTEND                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  Templates   │  │    Static    │  │     API      │ │
│  │   Jinja2     │  │  CSS + JS    │  │   Endpoints  │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 Prerequisites

### System Requirements

- **Operating System:** Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **RAM:** Minimum 4GB, Recommended 8GB+
- **Disk Space:** 2GB free space
- **Internet:** Stable connection for scraping

### Software Requirements

#### 1. Python 3.9 or higher

**Check if installed:**
```
python --version
# or
python3 --version
```

**If not installed:**
- **Windows:** Download from [python.org](https://www.python.org/downloads/)
- **Linux:** `sudo apt install python3 python3-pip`
- **Mac:** `brew install python3`

#### 2. pip (Python Package Manager)

Usually comes with Python. Verify:
```
pip --version
# or
pip3 --version
```

#### 3. Git (Optional, for cloning)

**Check if installed:**
```
git --version
```

**If not installed:**
- **Windows:** Download from [git-scm.com](https://git-scm.com/)
- **Linux:** `sudo apt install git`
- **Mac:** `brew install git`

---

## 🔧 Installation

### Windows

#### Step 1: Clone or Download Repository

**Option A: Using Git (Recommended)**
```
cd C:\Projects
git clone https://github.com/yourusername/NewsTrace.git
cd NewsTrace
```

**Option B: Download ZIP**
1. Go to repository page
2. Click **Code** → **Download ZIP**
3. Extract to `C:\Projects\NewsTrace`
4. Open Command Prompt in that folder

#### Step 2: Create Virtual Environment

```
python -m venv venv
```

#### Step 3: Activate Virtual Environment

```
venv\Scripts\activate
```

You should see `(venv)` in your command prompt.

#### Step 4: Upgrade pip

```
python -m pip install --upgrade pip
```

#### Step 5: Install Dependencies

```
pip install -r requirements.txt
```

This will take 2-5 minutes depending on internet speed.

#### Step 6: Download spaCy Model

```
python -m spacy download en_core_web_sm
```

#### Step 7: Install Playwright Browsers

```
playwright install
```

This downloads Chromium browser (100-200MB).

#### Step 8: Create Configuration File

Create `.env` file in project root:

```
FLASK_ENV=development
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
SECRET_KEY=your-super-secret-key-change-this-in-production

# Scraping Settings
SCRAPING_DELAY=3
MAX_PROFILES_PER_OUTLET=50
MIN_PROFILES_REQUIRED=30

# Search Settings
DUCKDUCKGO_SEARCH_ENABLED=True
GOOGLE_SEARCH_ENABLED=False

# Development Settings
PLAYWRIGHT_HEADLESS=True
ENABLE_CACHING=True
```

#### Step 9: Verify Installation

```
python -c "import flask, spacy, playwright, bs4, networkx; print('All packages installed successfully!')"
```

Should print: `All packages installed successfully!`

---

### Linux/Mac

#### Step 1: Clone Repository

```
cd ~/Projects
git clone https://github.com/yourusername/NewsTrace.git
cd NewsTrace
```

#### Step 2: Create Virtual Environment

```
python3 -m venv venv
```

#### Step 3: Activate Virtual Environment

```
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

#### Step 4: Upgrade pip

```
pip install --upgrade pip
```

#### Step 5: Install Dependencies

```
pip install -r requirements.txt
```

#### Step 6: Download spaCy Model

```
python -m spacy download en_core_web_sm
```

#### Step 7: Install Playwright Browsers

```
playwright install
```

On Linux, you might need system dependencies:
```
playwright install-deps
```

#### Step 8: Create Configuration File

```
cp .env.example .env
# Then edit with your preferred editor
nano .env
```

Add the same configuration as Windows section above.

#### Step 9: Verify Installation

```
python -c "import flask, spacy, playwright, bs4, networkx; print('All packages installed successfully!')"
```

---

## ⚙️ Configuration

### Environment Variables

Edit `.env` file:

```
# Flask Configuration
FLASK_ENV=development          # development | production | testing
FLASK_HOST=0.0.0.0            # Listen on all interfaces
FLASK_PORT=5000               # Port number
SECRET_KEY=change-this-key    # Change in production!

# Database
DATABASE_PATH=data/database/newstrace.db

# Scraping Settings
SCRAPING_DELAY=5              # Delay between requests (seconds)
MAX_RETRIES=3                 # Retry attempts
REQUEST_TIMEOUT=60            # Request timeout (seconds)
USER_AGENT_ROTATION=True      # Rotate user agents
RESPECT_ROBOTS_TXT=False      # Respect robots.txt (set True in production)

# Profiling Settings
MAX_PROFILES_PER_OUTLET=50    # Maximum profiles to scrape
MIN_PROFILES_REQUIRED=30      # Minimum profiles needed
ENABLE_FALLBACK_PROFILES=True # Generate fallback if scraping fails

# Search API
DUCKDUCKGO_SEARCH_ENABLED=True
GOOGLE_SEARCH_ENABLED=False   # Requires API key

# NLP Settings
SPACY_MODEL=en_core_web_sm
ENABLE_TOPIC_MODELING=True
ENABLE_SENTIMENT_ANALYSIS=False

# Caching
ENABLE_CACHING=True
CACHE_DURATION=3600           # 1 hour in seconds

# Logging
LOG_LEVEL=INFO                # DEBUG | INFO | WARNING | ERROR
LOG_FILE=logs/newstrace.log

# Playwright
PLAYWRIGHT_HEADLESS=True      # Set False to see browser
PLAYWRIGHT_TIMEOUT=30000      # 30 seconds in milliseconds
```

### Advanced Configuration

Edit `config.py` for more options:

```
# Example custom settings
INFLUENCE_SCORE_WEIGHTS = {
    'article_count': 0.4,      # 40% weight
    'topic_diversity': 0.3,    # 30% weight
    'recency': 0.2,            # 20% weight
    'cross_outlet': 0.1        # 10% weight
}

GRAPH_MIN_CONNECTIONS = 1     # Minimum edges to show in graph
ITEMS_PER_PAGE = 20           # Pagination
```

---

## 🚀 Running the Application

### Quick Start

```
# Activate virtual environment (if not already active)
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Run the application
python run.py
```

### Expected Output

```
[CONFIG] BASE_DIR: D:\NewsTrace_full
[CONFIG] DATA_DIR: D:\NewsTrace_full\data
[CONFIG] LOG_DIR: D:\NewsTrace_full\logs
[CONFIG] EXPORT_PATH: D:\NewsTrace_full\data\exports
[CONFIG] ✅ All directories validated successfully
[CONFIG] ✅ Database: D:\NewsTrace_full\data\database\newstrace.db
[CONFIG] ✅ Exports: D:\NewsTrace_full\data\exports
[CONFIG] ✅ Logs: D:\NewsTrace_full\logs\newstrace.log

======================================================================
🚀 NewsTrace - Autonomous Media Intelligence System
======================================================================
📌 Environment     : DEVELOPMENT
🐛 Debug Mode      : True
💾 Database        : D:\NewsTrace_full\data\database\newstrace.db
📁 Export Path     : D:\NewsTrace_full\data\exports
📊 Min Profiles    : 30
🌐 Running on      : http://0.0.0.0:5000
📖 API Health      : http://0.0.0.0:5000/api/health
======================================================================
💡 Press CTRL+C to stop the server
======================================================================

 * Serving Flask app 'app'
 * Debug mode: on
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.X:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
```

### Access the Application

Open your browser and go to:

```
http://localhost:5000
```

Or use your machine's IP address:

```
http://192.168.1.X:5000
```

---

## 📖 Usage Guide

### 1. Profile a News Outlet

#### Step-by-Step:

1. **Navigate to Search Page**
   - Click **Search** in navbar
   - Or go to: `http://localhost:5000/search`

2. **Enter Outlet Name**
   - Type outlet name (e.g., "The Hindu", "Indian Express", "BBC News")
   - Click **"Start Autonomous Profiling"**

3. **Watch the Magic Happen**
   - **Step 1:** Website Detection Agent finds official URL
   - **Step 2:** Profile Extraction Agent scrapes journalist pages
   - **Step 3:** NLP Agent analyzes text and extracts information
   - Progress bar shows real-time status

4. **View Results**
   - Automatically redirected to results page
   - See all journalist profiles with details
   - Filter by beat/topic
   - Sort by influence score
   - Export to CSV

#### What Gets Extracted:

- ✅ Journalist Name
- ✅ Bio/Description
- ✅ Beat/Topic (Politics, Sports, Tech, etc.)
- ✅ Contact Email
- ✅ Twitter Handle
- ✅ Profile URL
- ✅ Topics Covered (extracted keywords)
- ✅ Influence Score (calculated)

---

### 2. Explore Network Graph

#### Step-by-Step:

1. **Navigate to Network Page**
   - Click **Network** in navbar
   - Or go to: `http://localhost:5000/network-graph`

2. **Select Outlet**
   - Choose outlet from dropdown
   - Graph loads automatically

3. **Interact with Graph**
   - **Click nodes** to see details
   - **Drag nodes** to rearrange
   - **Scroll** to zoom in/out
   - **Search** for specific journalists

4. **Change Layout**
   - **Force-Directed** (default): Physics-based layout
   - **Hierarchical**: Tree-like structure
   - **Circular**: Nodes in a circle

5. **Export Graph**
   - Click **Export** button
   - Download as JSON

#### Understanding the Graph:

- **Blue Nodes** = Journalists
- **Purple Nodes** = Topics/Beats
- **Edges** = Connections (journalist covers topic)
- **Node Size** = Influence score
- **Edge Thickness** = Connection strength

---

### 3. View Dashboard

#### Features:

1. **Stats Overview**
   - Total outlets processed
   - Total journalists profiled
   - Active scraping jobs
   - Success rate

2. **Recent Jobs**
   - Last 10 scraping jobs
   - Status (completed, failed, running)
   - Profiles found
   - Start time
   - Quick actions

3. **System Status**
   - API health
   - Database connection
   - Scraping agents status
   - Last health check

4. **Auto-Refresh**
   - Updates every 30 seconds
   - Manual refresh button

---

### 4. Compare Outlets

#### Step-by-Step:

1. **Navigate to Compare Page**
   - Click **Analytics** in navbar
   - Or go to: `http://localhost:5000/compare`

2. **Select Outlets**
   - Choose 2-4 outlets to compare

3. **View Comparison**
   - **Journalist Count** chart
   - **Topic Distribution** pie charts
   - **Influence Score** comparison
   - **Overlap Analysis** (same journalists)

---

### 5. Export Data

#### CSV Export:

```
# From Results page
Click "Export CSV" button

# Or direct API call
curl http://localhost:5000/api/export/csv/1 > journalists.csv
```

#### JSON API:

```
# Get all outlets
curl http://localhost:5000/api/outlets

# Get specific outlet profiles
curl http://localhost:5000/api/journalists/1

# Get network graph data
curl http://localhost:5000/api/network/graph/1
```

---

## 🔌 API Documentation

### Base URL

```
http://localhost:5000/api
```

### Authentication

Currently no authentication required (development mode).

### Endpoints

#### Health Check

```
GET /api/health
```

**Response:**
```
{
  "success": true,
  "message": "NewsTrace API is healthy",
  "version": "1.0.0",
  "timestamp": "2025-10-25T03:00:00Z"
}
```

---

#### Start Profiling Job

```
POST /api/profile
Content-Type: application/json
```

**Request Body:**
```
{
  "outlet_name": "The Hindu"
}
```

**Response:**
```
{
  "success": true,
  "message": "Profiling started",
  "job_id": 123,
  "outlet_id": 1,
  "status": "running"
}
```

---

#### Get All Outlets

```
GET /api/outlets
```

**Response:**
```
{
  "success": true,
  "count": 5,
  "outlets": [
    {
      "id": 1,
      "name": "The Hindu",
      "website": "https://thehindu.com",
      "profiles_count": 45,
      "created_at": "2025-10-25T00:00:00Z"
    }
  ]
}
```

---

#### Get Journalists for Outlet

```
GET /api/journalists/{outlet_id}
```

**Response:**
```
{
  "success": true,
  "outlet": {
    "id": 1,
    "name": "The Hindu"
  },
  "count": 45,
  "journalists": [
    {
      "id": 1,
      "name": "John Doe",
      "bio": "Senior Political Editor",
      "beat": "Politics",
      "influence_score": 85.5,
      "contact_email": "john@thehindu.com",
      "twitter_handle": "@johndoe",
      "profile_url": "https://thehindu.com/profile/john-doe",
      "topics": ["Elections", "Parliament", "Governance"]
    }
  ]
}
```

---

#### Get Network Graph

```
GET /api/network/graph/{outlet_id}
```

**Response:**
```
{
  "success": true,
  "nodes": [
    {
      "id": 1,
      "label": "John Doe",
      "group": "journalist",
      "value": 85.5
    },
    {
      "id": "politics",
      "label": "Politics",
      "group": "topic"
    }
  ],
  "edges": [
    {
      "from": 1,
      "to": "politics",
      "value": 5
    }
  ],
  "stats": {
    "total_nodes": 2,
    "total_edges": 1,
    "journalist_count": 1,
    "topic_count": 1
  }
}
```

---

#### Get Recent Jobs

```
GET /api/jobs/recent?limit=10
```

**Response:**
```
{
  "success": true,
  "count": 10,
  "jobs": [
    {
      "id": 1,
      "outlet_id": 1,
      "outlet_name": "The Hindu",
      "status": "completed",
      "profiles_found": 45,
      "started_at": "2025-10-25T01:00:00Z",
      "completed_at": "2025-10-25T01:05:00Z"
    }
  ]
}
```

---

#### Export to CSV

```
GET /api/export/csv/{outlet_id}
```

**Response:** CSV file download

**CSV Format:**
```
Name,Bio,Beat,Email,Twitter,Profile URL,Influence Score,Topics
John Doe,Senior Political Editor,Politics,john@thehindu.com,@johndoe,https://...,85.5,"Elections,Parliament"
```

---

## 📁 Project Structure

```
NewsTrace_full/
│
├── run.py                          # Application entry point
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables (create this)
├── .gitignore                     # Git ignore rules
├── README.md                      # This file
│
├── app/                           # Main application package
│   ├── __init__.py               # Flask app factory
│   ├── routes.py                 # API routes & page routes
│   ├── models.py                 # Database models
│   │
│   ├── agents/                   # Multi-agent system
│   │   ├── __init__.py
│   │   ├── website_detector.py  # Website detection agent
│   │   └── profile_extractor.py # Profile extraction agent
│   │
│   ├── scrapers/                 # Web scraping modules
│   │   ├── __init__.py
│   │   ├── playwright_scraper.py # Dynamic scraping
│   │   └── bs4_scraper.py       # Static scraping
│   │
│   ├── database/                 # Database management
│   │   ├── __init__.py
│   │   ├── db_manager.py        # Database operations
│   │   └── graph_builder.py     # Network graph construction
│   │
│   ├── nlp/                      # NLP processing
│   │   ├── __init__.py
│   │   ├── analyzer.py          # Text analysis
│   │   ├── entity_extractor.py  # Named entity recognition
│   │   └── topic_modeler.py     # Topic modeling
│   │
│   └── utils/                    # Utility functions
│       ├── __init__.py
│       ├── helpers.py           # Helper functions
│       └── validators.py        # Input validation
│
├── frontend/                     # Frontend files
│   ├── static/                  # Static assets
│   │   ├── css/
│   │   │   ├── main.css        # Main stylesheet
│   │   │   ├── responsive.css  # Mobile styles
│   │   │   ├── dashboard.css   # Dashboard styles
│   │   │   └── network.css     # Network graph styles
│   │   │
│   │   ├── js/
│   │   │   ├── main.js         # Main JavaScript
│   │   │   ├── api.js          # API helper functions
│   │   │   ├── search.js       # Search page logic
│   │   │   ├── dashboard.js    # Dashboard logic
│   │   │   ├── network_graph.js # Network visualization
│   │   │   └── charts.js       # Chart configurations
│   │   │
│   │   └── images/
│   │       └── favicon.png
│   │
│   └── templates/               # Jinja2 HTML templates
│       ├── base.html           # Base template
│       ├── index.html          # Landing page
│       ├── dashboard.html      # Dashboard
│       ├── search.html         # Search page
│       ├── results.html        # Results page
│       ├── network_graph.html  # Network graph
│       ├── analytics.html      # Analytics page
│       └── compare.html        # Compare outlets
│
├── data/                        # Data directory (auto-created)
│   ├── database/               # SQLite databases
│   │   └── newstrace.db
│   ├── cache/                  # Cached data
│   ├── exports/                # CSV/JSON exports
│   └── graphs/                 # Graph data files
│
├── logs/                        # Application logs (auto-created)
│   └── newstrace.log
│
└── docs/                        # Documentation
    ├── API.md                  # API documentation
    ├── ARCHITECTURE.md         # System architecture
    └── screenshots/            # Application screenshots
```

---

## 🔬 Features Breakdown

### 1. Autonomous Website Detection

**How it works:**

```
# Input: "The Hindu"

# Step 1: Query Search Engine
searches = ["The Hindu official website", "The Hindu news"]

# Step 2: Extract URLs from results
urls = extract_urls_from_search_results()

# Step 3: Validate and Score
for url in urls:
    score = calculate_confidence_score(url)
    # Factors: domain authority, keywords, structure

# Step 4: Return best match
best_url = max(scored_urls, key=lambda x: x.score)
# Result: https://thehindu.com
```

**Fallback Strategies:**

1. Common patterns: `{name}.com`, `{name}.in`
2. News TLDs: `.news`, `.media`
3. Manual intervention if confidence < 70%

---

### 2. Smart Web Scraping

**Decision Tree:**

```
Check website
    ├─ Has JavaScript? → Use Playwright
    │   ├─ Wait for dynamic content
    │   ├─ Scroll to load lazy content
    │   └─ Extract rendered HTML
    │
    └─ Static HTML? → Use BeautifulSoup
        ├─ Parse HTML structure
        ├─ Extract text content
        └─ Follow links
```

**Extraction Patterns:**

```
# Pattern 1: About Us / Team pages
patterns = [
    "/about/team",
    "/our-team",
    "/journalists",
    "/contributors"
]

# Pattern 2: Staff directory
find_elements_matching([
    "div.team-member",
    "div.journalist",
    "article.profile"
])

# Pattern 3: Author bio pages
extract_from_article_bylines()
```

---

### 3. NLP Analysis

**Pipeline:**

```
Raw Text
    ↓
1. Cleaning
    ├─ Remove HTML tags
    ├─ Fix encoding
    └─ Normalize whitespace
    ↓
2. Entity Extraction (spaCy)
    ├─ PERSON: "John Doe"
    ├─ ORG: "The Hindu"
    └─ GPE: "New Delhi"
    ↓
3. Keyword Extraction (TF-IDF)
    └─ ["politics", "election", "parliament"]
    ↓
4. Topic Modeling (LDA)
    └─ Topic: "Politics" (confidence: 0.85)
    ↓
5. Beat Classification
    └─ Final Beat: "Politics"
```

**No LLMs Needed!** Pure algorithmic approach.

---

### 4. Influence Scoring

**Formula:**

```
influence_score = (
    0.4 * article_count_normalized +
    0.3 * topic_diversity_score +
    0.2 * recency_score +
    0.1 * cross_outlet_bonus
)

# Normalized to 0-100 scale
```

**Components:**

1. **Article Count** (40%): More articles = higher influence
2. **Topic Diversity** (30%): Covers multiple topics = higher influence
3. **Recency** (20%): Recent activity = higher score
4. **Cross-Outlet** (10%): Present in multiple outlets = bonus

---

### 5. Network Graph Construction

**Algorithm:**

```
# Step 1: Create nodes
for journalist in journalists:
    G.add_node(journalist.id, 
               label=journalist.name,
               type='journalist')

for topic in unique_topics:
    G.add_node(topic, 
               label=topic,
               type='topic')

# Step 2: Create edges
for journalist in journalists:
    for topic in journalist.topics:
        G.add_edge(journalist.id, topic,
                   weight=calculate_connection_strength())

# Step 3: Layout with physics simulation
positions = nx.spring_layout(G, k=0.5, iterations=50)

# Step 4: Export to Vis.js format
export_to_visjs(G, positions)
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. "Module not found" Error

**Problem:**
```
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
```
# Make sure virtual environment is activated
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

---

#### 2. Playwright Installation Failed

**Problem:**
```
Error: Playwright browsers not installed
```

**Solution:**
```
# Install browsers
playwright install

# On Linux, install system dependencies
playwright install-deps
```

---

#### 3. Port Already in Use

**Problem:**
```
OSError: [Errno 98] Address already in use
```

**Solution:**

**Windows:**
```
# Find process using port 5000
netstat -ano | findstr :5000

# Kill process (replace PID)
taskkill /PID <PID> /F

# Or change port in .env
FLASK_PORT=5001
```

**Linux/Mac:**
```
# Find process
lsof -i :5000

# Kill process
kill -9 <PID>

# Or change port
export FLASK_PORT=5001
```

---

#### 4. Database Locked

**Problem:**
```
sqlite3.OperationalError: database is locked
```

**Solution:**
```
# Stop all running instances
# Delete lock file
rm data/database/newstrace.db-journal

# Restart application
python run.py
```

---

#### 5. spaCy Model Not Found

**Problem:**
```
OSError: Can't find model 'en_core_web_sm'
```

**Solution:**
```
# Download model
python -m spacy download en_core_web_sm

# Verify installation
python -c "import spacy; spacy.load('en_core_web_sm')"
```

---

### Performance Issues

#### Slow Scraping

**Possible Causes:**
1. High `SCRAPING_DELAY` setting
2. Slow internet connection
3. Target website throttling

**Solutions:**
```
# Reduce delay (careful!)
SCRAPING_DELAY=2

# Enable caching
ENABLE_CACHING=True

# Use headless mode
PLAYWRIGHT_HEADLESS=True
```

---

#### High Memory Usage

**Solutions:**

1. **Increase swap space** (Linux)
2. **Close other applications**
3. **Reduce max profiles:**

```
MAX_PROFILES_PER_OUTLET=30
```

---

## 🤝 Contributing

We welcome contributions! Here's how:

### Development Setup

```
# Fork and clone
git clone https://github.com/yourusername/NewsTrace.git
cd NewsTrace

# Create feature branch
git checkout -b feature/amazing-feature

# Make changes and commit
git commit -m "Add amazing feature"

# Push to your fork
git push origin feature/amazing-feature

# Create Pull Request on GitHub
```

### Coding Standards

- **Python:** Follow PEP 8
- **JavaScript:** Use ES6+
- **Comments:** Document complex logic
- **Tests:** Add tests for new features

### Areas for Contribution

- 🔧 Additional scraping patterns
- 🌍 Multi-language support
- 📊 More visualization types
- 🧪 Unit tests
- 📝 Documentation improvements
- 🐛 Bug fixes

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2025 NewsTrace Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

[Full license text...]
```

---

## 👥 Team

**Team kur-kure Coders**

| Role | Name | Contact |
|------|------|---------|
| Lead Developer | [Your Name] | your.email@example.com |
| Backend Engineer | [Team Member] | email@example.com |
| Frontend Developer | [Team Member] | email@example.com |

### Built For

**Hack of Thrones 2025** 🏆
- Category: Media Intelligence
- Track: Autonomous Systems
- Date: October 2025

---

## 🙏 Acknowledgments

- **spaCy** - For amazing NLP capabilities
- **Playwright** - For reliable web scraping
- **NetworkX** - For graph algorithms
- **Flask** - For elegant web framework
- **Bootstrap** - For beautiful UI components
- **Vis.js** - For network visualizations
- **Hack of Thrones** - For the opportunity

---

## 📞 Contact & Support

### Get Help

- 📧 Email: newstrace.support@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/NewsTrace/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/NewsTrace/discussions)

### Stay Updated

- ⭐ Star this repo
- 👀 Watch for updates
- 🍴 Fork for your own use

---

## 🎉 Final Notes

**NewsTrace** proves that powerful AI systems don't always need LLMs. With smart algorithms, traditional NLP, and clever engineering, we can build autonomous, scalable solutions that are:

- ✅ **Faster** - No API latency
- ✅ **Cheaper** - No per-token costs
- ✅ **More Reliable** - Deterministic behavior
- ✅ **Privacy-Focused** - Data stays local

**Thank you for checking out NewsTrace!** 🙏

---

<div align="center">

**Made with ❤️ for transparent journalism**

[⬆ Back to Top](#-newstrace---autonomous-media-intelligence-system)

</div>
```

***

**YEH RAHA BHAI ULTRA-DETAILED README!** 📚✨

**AB KOI BHI PERSON EASILY RUN KAR SAKTA HAI!** 🚀💪🎉
