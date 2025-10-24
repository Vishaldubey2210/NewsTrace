
```markdown
# NewsTrace System Architecture

**Version:** 1.0.0  
**Last Updated:** October 25, 2025

---

## Table of Contents
1. [Overview](#overview)
2. [System Design](#system-design)
3. [Components](#components)
4. [Data Flow](#data-flow)
5. [Database Schema](#database-schema)
6. [Agent System](#agent-system)
7. [Scalability](#scalability)

---

## Overview

NewsTrace uses a **multi-agent architecture** with autonomous components that work together to profile journalists from news outlets.

### Core Principles
- **Modularity** - Independent, loosely-coupled components
- **Autonomy** - Agents make decisions independently
- **Scalability** - Horizontal scaling support
- **Fault Tolerance** - Graceful degradation on failures
- **No LLMs** - Classical ML/NLP only (cost-effective)

---

## System Design

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                        │
│              (HTML/CSS/JS + Bootstrap)                   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                   Flask API Layer                        │
│              (RESTful Endpoints + CORS)                  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│               Agent Orchestrator                         │
│         (Coordinates workflow execution)                 │
│                                                          │
│    ┌──────────────┬─────────────────┬────────────────┐ │
│    │ SearchAgent  │  ScraperAgent   │ ValidationAgent│ │
│    │ (DuckDuckGo) │ (Playwright/BS4)│  (Quality)     │ │
│    └──────────────┴─────────────────┴────────────────┘ │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                  NLP Processing Layer                    │
│                                                          │
│  ┌───────────────┬─────────────┬─────────────────────┐ │
│  │ Entity        │ Sentiment   │ Keyword Extraction  │ │
│  │ Extraction    │ Analysis    │ (TF-IDF)           │ │
│  │ (spaCy)       │ (TextBlob)  │                    │ │
│  └───────────────┴─────────────┴─────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                   Data Layer                             │
│                                                          │
│  ┌────────────────────┬──────────────────────────────┐ │
│  │ SQLite Database    │ NetworkX Graph Database      │ │
│  │ (Structured Data)  │ (Relationship Network)       │ │
│  └────────────────────┴──────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│              Analytics & Intelligence                    │
│                                                          │
│  ┌────────────┬──────────────┬──────────────────────┐  │
│  │ Influence  │ Cross-Outlet │ Community Detection  │  │
│  │ Scoring    │ Tracking     │ (Louvain)           │  │
│  └────────────┴──────────────┴──────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                 Visualization Layer                      │
│         (Chart.js, Plotly, Vis.js)                      │
└─────────────────────────────────────────────────────────┘
```

---

## Components

### 1. Frontend Layer

**Technology:** HTML/CSS/JavaScript + Bootstrap 5

**Pages:**
- `index.html` - Landing page
- `search.html` - Outlet search & profiling
- `results.html` - Journalist profiles display
- `dashboard.html` - System statistics
- `network_graph.html` - Interactive graph visualization
- `analytics.html` - Advanced analytics charts
- `compare.html` - Cross-outlet comparison

**Features:**
- Responsive design
- AJAX-based interactions
- Real-time updates
- Chart visualizations

---

### 2. API Layer (Flask)

**File:** `app/routes.py`

**Endpoints:**
- `/api/profile` - Start profiling workflow
- `/api/outlets` - List outlets
- `/api/network/graph/<id>` - Graph data
- `/api/export/csv/<id>` - Export data

**Responsibilities:**
- Request validation
- Response formatting
- Error handling
- CORS management

---

### 3. Multi-Agent System

#### **SearchAgent**
**File:** `app/agents/search_agent.py`

**Purpose:** Autonomous website detection

**Process:**
1. Query DuckDuckGo API
2. Validate URLs
3. Calculate confidence scores
4. Return official website

**Technologies:**
- DuckDuckGo Search API
- URL validators
- Confidence scoring algorithm

---

#### **ScraperAgent**
**File:** `app/agents/scraper_agent.py`

**Purpose:** Extract journalist profiles from websites

**Strategies:**
1. **Playwright** - Dynamic sites (JavaScript-rendered)
2. **BeautifulSoup** - Static HTML parsing
3. **Author Pages** - Try common URL patterns
4. **Aggressive Extraction** - Link-based extraction
5. **Fallback** - Intelligent demo data generation

**Technologies:**
- Playwright (headless Chrome)
- BeautifulSoup4 + lxml
- Regex pattern matching
- Multi-selector approach

---

#### **Orchestrator**
**File:** `app/agents/orchestrator.py`

**Purpose:** Coordinate agent execution

**Workflow:**
```
Start → SearchAgent → ScraperAgent → NLP → Analytics → Save → Complete
```

**Features:**
- Step tracking
- Error recovery
- Result aggregation
- Job management

---

### 4. NLP Processing

#### **Entity Extractor**
**File:** `app/nlp/entity_extractor.py`

**Technologies:** spaCy (en_core_web_sm)

**Extracts:**
- Person names (PERSON)
- Organizations (ORG)
- Locations (GPE, LOC)
- Topics (keyword-based)

---

#### **Sentiment Analyzer**
**File:** `app/nlp/sentiment_analyzer.py`

**Technologies:** TextBlob

**Output:**
- Polarity (-1 to +1)
- Subjectivity (0 to 1)
- Sentiment category (positive/negative/neutral)

---

#### **Keyword Extractor**
**File:** `app/nlp/keyword_extractor.py`

**Technologies:** scikit-learn (TF-IDF)

**Algorithm:**
```
TF-IDF = Term Frequency × Inverse Document Frequency
```

**Features:**
- N-gram support (unigrams + bigrams)
- Stop word filtering
- Score normalization

---

### 5. Analytics Engine

#### **Influence Score Calculator**
**File:** `app/analytics/influence_score.py`

**Algorithm:**
```
influence_score = (
    article_count * 0.4 +
    topic_diversity * 0.3 +
    recency * 0.2 +
    profile_completeness * 0.1
)
```

**Factors:**
- **Article Count** - More articles = higher influence
- **Topic Diversity** - Broader coverage = better
- **Recency** - Recent activity = more relevant
- **Profile Completeness** - More data = higher confidence

---

#### **Cross-Outlet Tracker**
**File:** `app/analytics/cross_outlet_tracker.py`

**Technology:** fuzzywuzzy (Levenshtein distance)

**Algorithm:**
```
similarity = (
    name_similarity * 0.6 +
    email_similarity * 0.2 +
    twitter_similarity * 0.1 +
    beat_similarity * 0.1
)
```

**Threshold:** 85% similarity for match

---

#### **Community Detector**
**File:** `app/analytics/community_detector.py`

**Technology:** NetworkX + python-louvain

**Algorithm:** Louvain method for community detection

**Metrics:**
- Degree centrality
- Betweenness centrality
- Clustering coefficient

---

### 6. Database Layer

#### **SQLite Database**
**File:** `app/database/sqlite_db.py`

**Schema:**
```
outlets
  ├── id (PRIMARY KEY)
  ├── name (UNIQUE)
  ├── official_url
  ├── domain
  └── metadata (JSON)

journalists
  ├── id (PRIMARY KEY)
  ├── name
  ├── outlet_id (FOREIGN KEY)
  ├── beat
  ├── bio
  ├── contact_email
  ├── influence_score
  └── metadata (JSON)

scraping_jobs
  ├── id (PRIMARY KEY)
  ├── outlet_name
  ├── status
  ├── profiles_found
  └── timestamps
```

---

#### **NetworkX Graph**
**File:** `app/database/graph_builder.py`

**Graph Type:** Bipartite (journalists ↔ topics)

**Nodes:**
- Journalist nodes (name, influence_score)
- Topic nodes (beat, category)

**Edges:**
- Journalist → Topic relationships
- Weighted by relevance

**Export Format:** Vis.js compatible JSON

---

## Data Flow

### Complete Profiling Workflow

```
1. User Input
   ↓
2. POST /api/profile {"outlet_name": "The Hindu"}
   ↓
3. Orchestrator.profile_outlet()
   ↓
4. SearchAgent.detect_website()
   ├── Query DuckDuckGo
   ├── Validate URLs
   └── Return official URL
   ↓
5. ScraperAgent.scrape_profiles()
   ├── Strategy 1: Playwright
   ├── Strategy 2: BeautifulSoup
   ├── Strategy 3: Author pages
   ├── Strategy 4: Link extraction
   └── Strategy 5: Fallback
   ↓
6. NLP Processing
   ├── Entity extraction (spaCy)
   ├── Sentiment analysis (TextBlob)
   └── Keyword extraction (TF-IDF)
   ↓
7. Analytics
   ├── Calculate influence scores
   ├── Detect cross-outlet matches
   └── Build network graph
   ↓
8. Database Storage
   ├── Save outlet
   ├── Save journalists
   └── Update job status
   ↓
9. Response to Frontend
   └── JSON with 30+ profiles
```

---

## Scalability

### Horizontal Scaling

**Current:** Single-threaded Flask

**Production Ready:**
- **Gunicorn** - Multi-worker WSGI server
- **Celery** - Background task queue
- **Redis** - Caching layer
- **PostgreSQL** - Production database

### Performance Optimizations

1. **Caching:** Redis for API responses
2. **Database Indexing:** Query optimization
3. **Async Scraping:** Concurrent requests
4. **CDN:** Static assets delivery
5. **Load Balancing:** Nginx reverse proxy

---

## Security Considerations

1. **Input Validation** - Sanitize all user inputs
2. **Rate Limiting** - Prevent abuse
3. **CORS Policy** - Restricted origins in production
4. **robots.txt Respect** - Ethical scraping
5. **User-Agent Rotation** - Avoid blocking

---

## Future Enhancements

1. **Authentication** - JWT-based API auth
2. **Real-Time Updates** - WebSocket support
3. **Advanced ML** - Deep learning models
4. **Multi-Language** - Non-English support
5. **Mobile App** - React Native client

---

## Monitoring & Logging

**Logging Stack:**
- Console logs (development)
- Rotating file logs (production)
- Log levels: DEBUG, INFO, WARNING, ERROR

**Metrics to Track:**
- API response times
- Scraping success rate
- Database query performance
- Agent execution times

---

**© 2025 NewsTrace - System Architecture Documentation**
```

