# NewsTrace Deployment & Production Operations Guide

## Production Environment Prerequisites
- Python 3.10+
- SQLite3 or PostgreSQL
- 2GB RAM minimum for NLP Spacy models

## Deployment via Docker
```bash
docker compose up -d --build
```

## Deployment on Cloud (Render / AWS / GCP)
Set the following environment variables:
- `FLASK_ENV=production`
- `SECRET_KEY=your_production_secret_key`
- `PORT=5000`
- `DATABASE_PATH=data/newstrace.db`
