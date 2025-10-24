

## 📄 **Create File: `docs/API.md`**

**Path:** `NewsTrace_full/docs/API.md`

```markdown
# NewsTrace API Documentation

**Version:** 1.0.0  
**Base URL:** `http://localhost:5000/api`  
**Last Updated:** October 25, 2025

---

## Table of Contents
1. [Authentication](#authentication)
2. [Core Endpoints](#core-endpoints)
3. [Analytics Endpoints](#analytics-endpoints)
4. [Export Endpoints](#export-endpoints)
5. [Utility Endpoints](#utility-endpoints)
6. [Error Handling](#error-handling)

---

## Authentication

Currently **no authentication required** (development mode).

For production, implement JWT tokens or API keys.

---

## Core Endpoints

### 1. Start Profiling Workflow

**Endpoint:** `POST /api/profile`

**Description:** Start autonomous profiling for a news outlet.

**Request Body:**
```
{
  "outlet_name": "The Hindu"
}
```

**Response (200 OK):**
```
{
  "success": true,
  "outlet_name": "The Hindu",
  "outlet_id": 1,
  "profile_count": 35,
  "profiles": [
    {
      "id": 1,
      "name": "Rajesh Kumar",
      "beat": "Politics",
      "bio": "Senior political correspondent with 10+ years experience",
      "contact_email": "rajesh.kumar@thehindu.com",
      "profile_url": "https://www.thehindu.com/profile/rajesh-kumar",
      "twitter_handle": "@RajeshKumar",
      "influence_score": 85.5
    }
  ],
  "started_at": "2025-10-25T01:00:00",
  "completed_at": "2025-10-25T01:00:30",
  "steps": [
    {
      "agent": "SearchAgent",
      "status": "completed",
      "success": true,
      "duration": 2.5
    },
    {
      "agent": "ScraperAgent",
      "status": "completed",
      "success": true,
      "duration": 25.3
    }
  ]
}
```

**Error Response (500):**
```
{
  "success": false,
  "error": "Website detection failed",
  "outlet_name": "The Hindu"
}
```

---

### 2. Get All Outlets

**Endpoint:** `GET /api/outlets`

**Description:** Retrieve all registered news outlets.

**Response (200 OK):**
```
{
  "success": true,
  "count": 5,
  "outlets": [
    {
      "id": 1,
      "name": "The Hindu",
      "official_url": "https://www.thehindu.com",
      "domain": "www.thehindu.com",
      "total_journalists": 35,
      "status": "active",
      "last_scraped": "2025-10-25T01:00:00"
    },
    {
      "id": 2,
      "name": "Indian Express",
      "official_url": "https://indianexpress.com",
      "domain": "indianexpress.com",
      "total_journalists": 42,
      "status": "active",
      "last_scraped": "2025-10-25T00:30:00"
    }
  ]
}
```

---

### 3. Get Single Outlet

**Endpoint:** `GET /api/outlet/<outlet_id>`

**Example:** `GET /api/outlet/1`

**Response (200 OK):**
```
{
  "success": true,
  "outlet": {
    "id": 1,
    "name": "The Hindu",
    "official_url": "https://www.thehindu.com",
    "domain": "www.thehindu.com",
    "total_journalists": 35,
    "last_scraped": "2025-10-25T01:00:00"
  }
}
```

**Error (404):**
```
{
  "success": false,
  "error": "Outlet not found"
}
```

---

### 4. Get Journalists by Outlet

**Endpoint:** `GET /api/outlet/<outlet_id>/journalists`

**Example:** `GET /api/outlet/1/journalists`

**Response (200 OK):**
```
{
  "success": true,
  "count": 35,
  "journalists": [
    {
      "id": 1,
      "name": "Rajesh Kumar",
      "outlet_id": 1,
      "beat": "Politics",
      "bio": "Senior political correspondent...",
      "contact_email": "rajesh.kumar@thehindu.com",
      "contact_phone": null,
      "profile_url": "https://www.thehindu.com/profile/rajesh-kumar",
      "twitter_handle": "@RajeshKumar",
      "linkedin_url": null,
      "influence_score": 85.5,
      "metadata": {
        "topics": ["Politics", "Elections", "Parliament"]
      },
      "created_at": "2025-10-25T01:00:30",
      "updated_at": "2025-10-25T01:00:30"
    }
  ]
}
```

---

### 5. Get Network Graph Data

**Endpoint:** `GET /api/network/graph/<outlet_id>`

**Example:** `GET /api/network/graph/1`

**Description:** Get journalist-topic network graph data for Vis.js visualization.

**Response (200 OK):**
```
{
  "success": true,
  "nodes": [
    {
      "id": "Rajesh Kumar",
      "label": "Rajesh Kumar",
      "group": "journalist",
      "color": "#667eea"
    },
    {
      "id": "Politics",
      "label": "Politics",
      "group": "topic",
      "color": "#f093fb"
    }
  ],
  "edges": [
    {
      "from": "Rajesh Kumar",
      "to": "Politics"
    }
  ],
  "stats": {
    "total_nodes": 50,
    "total_edges": 35
  }
}
```

---

## Analytics Endpoints

### 6. Get Analytics Statistics

**Endpoint:** `GET /api/analytics/stats`

**Description:** Get overall system statistics.

**Response (200 OK):**
```
{
  "success": true,
  "stats": {
    "total_outlets": 5,
    "total_journalists": 150,
    "total_jobs": 10,
    "completed_jobs": 8,
    "failed_jobs": 2,
    "avg_influence_score": 72.5
  }
}
```

---

### 7. Get Top Journalists

**Endpoint:** `GET /api/journalists/top/<limit>`

**Example:** `GET /api/journalists/top/10`

**Parameters:**
- `limit` (integer): Number of journalists to return (default: 10, max: 50)

**Response (200 OK):**
```
{
  "success": true,
  "count": 10,
  "journalists": [
    {
      "id": 1,
      "name": "Rajesh Kumar",
      "outlet_id": 1,
      "beat": "Politics",
      "influence_score": 95.8,
      "profile_url": "https://www.thehindu.com/profile/rajesh-kumar"
    }
  ]
}
```

---

## Export Endpoints

### 8. Export CSV

**Endpoint:** `GET /api/export/csv/<outlet_id>`

**Example:** `GET /api/export/csv/1`

**Description:** Download journalist profiles as CSV file.

**Response:** File download (text/csv)

**Filename:** `journalists_outlet_1_20251025_010030.csv`

**CSV Columns:**
- Name
- Beat
- Bio
- Contact Email
- Profile URL
- Twitter Handle
- Influence Score

---

### 9. Export JSON

**Endpoint:** `GET /api/export/json/<outlet_id>`

**Example:** `GET /api/export/json/1`

**Description:** Download journalist profiles as JSON file.

**Response:** File download (application/json)

**Filename:** `journalists_outlet_1.json`

---

## Utility Endpoints

### 10. Recent Jobs

**Endpoint:** `GET /api/jobs/recent`

**Query Parameters:**
- `limit` (integer): Number of jobs to return (default: 10)

**Example:** `GET /api/jobs/recent?limit=5`

**Response (200 OK):**
```
{
  "success": true,
  "jobs": [
    {
      "id": 1,
      "outlet_name": "The Hindu",
      "status": "completed",
      "profiles_found": 35,
      "started_at": "2025-10-25T01:00:00",
      "completed_at": "2025-10-25T01:00:30",
      "error_message": null
    }
  ]
}
```

---

### 11. Get Job Details

**Endpoint:** `GET /api/jobs/<job_id>`

**Example:** `GET /api/jobs/1`

**Response (200 OK):**
```
{
  "success": true,
  "job": {
    "id": 1,
    "outlet_name": "The Hindu",
    "status": "completed",
    "profiles_found": 35,
    "started_at": "2025-10-25T01:00:00",
    "completed_at": "2025-10-25T01:00:30"
  }
}
```

---

### 12. Health Check

**Endpoint:** `GET /api/health`

**Description:** Check API health status.

**Response (200 OK):**
```
{
  "status": "healthy",
  "timestamp": "2025-10-25T01:00:00",
  "service": "NewsTrace API",
  "version": "1.0.0"
}
```

---

### 13. Website Detection Test

**Endpoint:** `POST /api/search/detect`

**Description:** Test website detection (for debugging).

**Request Body:**
```
{
  "outlet_name": "The Hindu"
}
```

**Response (200 OK):**
```
{
  "success": true,
  "url": "https://www.thehindu.com",
  "domain": "www.thehindu.com",
  "confidence": 0.9,
  "method": "duckduckgo"
}
```

---

## Error Handling

### Standard Error Response Format

All endpoints return errors in this format:

```
{
  "success": false,
  "error": "Error message here"
}
```

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid request parameters |
| 404 | Not Found | Resource not found |
| 500 | Internal Server Error | Server error |

### Common Error Messages

**400 Bad Request:**
```
{
  "success": false,
  "error": "No JSON data provided"
}
```

**404 Not Found:**
```
{
  "success": false,
  "error": "Outlet not found"
}
```

**500 Internal Server Error:**
```
{
  "success": false,
  "error": "Website detection failed"
}
```

---

## Rate Limiting

**Current:** No rate limiting (development mode)  
**Production:** Implement rate limiting (e.g., 100 requests/minute)

---

## CORS Policy

**Enabled for:** `/api/*` endpoints  
**Allowed Origins:** `*` (development)  
**Allowed Methods:** GET, POST, PUT, DELETE  
**Allowed Headers:** Content-Type

---

## Example Usage

### Using cURL

```
# Profile an outlet
curl -X POST http://localhost:5000/api/profile \
  -H "Content-Type: application/json" \
  -d '{"outlet_name": "The Hindu"}'

# Get all outlets
curl http://localhost:5000/api/outlets

# Get journalists
curl http://localhost:5000/api/outlet/1/journalists

# Export CSV
curl -O http://localhost:5000/api/export/csv/1
```

### Using JavaScript (Fetch API)

```
// Profile outlet
fetch('http://localhost:5000/api/profile', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ outlet_name: 'The Hindu' })
})
.then(res => res.json())
.then(data => console.log(data));

// Get outlets
fetch('http://localhost:5000/api/outlets')
.then(res => res.json())
.then(data => console.log(data.outlets));
```

### Using Python (requests)

```
import requests

# Profile outlet
response = requests.post(
    'http://localhost:5000/api/profile',
    json={'outlet_name': 'The Hindu'}
)
print(response.json())

# Get outlets
response = requests.get('http://localhost:5000/api/outlets')
print(response.json()['outlets'])
```

---

## Changelog

**v1.0.0 (2025-10-25)**
- Initial API release
- Core profiling endpoints
- Analytics endpoints
- Export functionality
- Network graph data

---

## Support

For issues or questions:
- GitHub: [NewsTrace Repository]
- Email: support@newstrace.com

---

**© 2025 NewsTrace - Media Intelligence System**
```

***

