# Light SQLite Service

A lightweight FastAPI service using SQLite to store and retrieve items. Ideal for quick prototyping or internal microservices with minimal dependencies.

## Features

- ✅ RESTful API with FastAPI
- ✅ SQLite storage (file-based, simple persistence)
- ✅ Auto-create table via `/init` endpoint
- ✅ Add items, list items, fetch item by ID

## Requirements

- Python 3.8+
- `FastAPI`
- `uvicorn`
- `requests` (for test script)

Install dependencies:

```bash
pip install fastapi uvicorn requests
