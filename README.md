# Deployment Guide

## What is Elasticsearch?

**Elasticsearch** is a fast, distributed search and analytics engine for JSON data.  
In this project, it powers full-text search: documents are **indexed** via the backend, and search queries retrieve relevant results for the frontend.

---

## Quick Start

### Prerequisites

- **Elasticsearch** running on `localhost:9200`
- **Python 3.8+**
- **npm** (for frontend dependencies; Vue.js is installed via `npm install`)

---

### Installing Requirements

#### Backend (Python)

From your backend directory, run:
```bash
pip install -r requirements.txt
```

#### Frontend (Vue.js)

From your `frontend` directory, run:
```bash
npm install
```
This will install Vue.js and all other frontend dependencies listed in `package.json`.

---

### Backend Setup

```bash
# Index data into Elasticsearch
python index_data.py

# Start the FastAPI backend
fastapi dev main.py
```

---

### Frontend Setup

```bash
cd frontend
npm run serve
```

---

### Access the App

- Frontend: [http://localhost:8080](http://localhost:8080)
- Backend:  [http://localhost:8000](http://localhost:8000)

---

## Demo

_Sample screenshots:_

![](screenshots/Screenshot1.png)
![](screenshots/Screenshot2.png)

---

## Improvements

- TBD

---

## Troubleshooting

- **Elasticsearch errors:** Ensure it’s running and accessible at `localhost:9200`.
- **Missing data file:** Check that your dataset (e.g., `apod.json`) exists in the expected location.
- **Dependency issues:** Make sure Python and npm dependencies are installed.

---

## Useful Links

- [Elasticsearch Docs](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Vue.js Docs](https://vuejs.org/)