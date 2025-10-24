-- ============================================
-- NewsTrace Database Schema (SQLite)
-- ============================================

-- ==================== OUTLETS TABLE ====================
CREATE TABLE IF NOT EXISTS outlets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    official_url TEXT,
    domain TEXT,
    detected_at TEXT DEFAULT (datetime('now')),
    last_scraped TEXT,
    total_journalists INTEGER DEFAULT 0,
    status TEXT DEFAULT 'active',
    metadata TEXT
);

-- ==================== JOURNALISTS TABLE ====================
CREATE TABLE IF NOT EXISTS journalists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    outlet_id INTEGER NOT NULL,
    beat TEXT,
    contact_email TEXT,
    contact_phone TEXT,
    bio TEXT,
    profile_url TEXT,
    twitter_handle TEXT,
    linkedin_url TEXT,
    first_seen TEXT DEFAULT (datetime('now')),
    last_updated TEXT DEFAULT (datetime('now')),
    article_count INTEGER DEFAULT 0,
    influence_score REAL DEFAULT 0.0,
    metadata TEXT,
    FOREIGN KEY (outlet_id) REFERENCES outlets(id) ON DELETE CASCADE
);

-- ==================== ARTICLES TABLE ====================
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    journalist_id INTEGER NOT NULL,
    outlet_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    url TEXT UNIQUE,
    published_date TEXT,
    category TEXT,
    keywords TEXT,
    sentiment_score REAL,
    word_count INTEGER,
    scraped_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (journalist_id) REFERENCES journalists(id) ON DELETE CASCADE,
    FOREIGN KEY (outlet_id) REFERENCES outlets(id) ON DELETE CASCADE
);

-- ==================== TOPICS TABLE ====================
CREATE TABLE IF NOT EXISTS topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    keywords TEXT,
    article_count INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now'))
);

-- ==================== JOURNALIST-TOPICS RELATIONSHIP ====================
CREATE TABLE IF NOT EXISTS journalist_topics (
    journalist_id INTEGER NOT NULL,
    topic_id INTEGER NOT NULL,
    article_count INTEGER DEFAULT 0,
    relevance_score REAL DEFAULT 0.0,
    PRIMARY KEY (journalist_id, topic_id),
    FOREIGN KEY (journalist_id) REFERENCES journalists(id) ON DELETE CASCADE,
    FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE
);

-- ==================== SCRAPING JOBS TABLE ====================
CREATE TABLE IF NOT EXISTS scraping_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    outlet_name TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    profiles_found INTEGER DEFAULT 0,
    started_at TEXT,
    completed_at TEXT,
    error_message TEXT,
    metadata TEXT
);

-- ==================== CROSS-OUTLET MATCHES TABLE ====================
CREATE TABLE IF NOT EXISTS cross_outlet_matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    journalist1_id INTEGER NOT NULL,
    journalist2_id INTEGER NOT NULL,
    match_score REAL DEFAULT 0.0,
    match_type TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (journalist1_id) REFERENCES journalists(id) ON DELETE CASCADE,
    FOREIGN KEY (journalist2_id) REFERENCES journalists(id) ON DELETE CASCADE
);

-- ==================== INDEXES FOR PERFORMANCE ====================
CREATE INDEX IF NOT EXISTS idx_journalists_outlet ON journalists(outlet_id);
CREATE INDEX IF NOT EXISTS idx_journalists_name ON journalists(name);
CREATE INDEX IF NOT EXISTS idx_journalists_influence ON journalists(influence_score DESC);
CREATE INDEX IF NOT EXISTS idx_articles_journalist ON articles(journalist_id);
CREATE INDEX IF NOT EXISTS idx_articles_outlet ON articles(outlet_id);
CREATE INDEX IF NOT EXISTS idx_articles_date ON articles(published_date);
CREATE INDEX IF NOT EXISTS idx_journalist_topics_journalist ON journalist_topics(journalist_id);
CREATE INDEX IF NOT EXISTS idx_journalist_topics_topic ON journalist_topics(topic_id);
CREATE INDEX IF NOT EXISTS idx_scraping_jobs_status ON scraping_jobs(status);
