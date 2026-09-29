# Tech Interview 1: Marketing Campaign API

## Overview

This exercise contains an LLM-generated, partially-implemented Marketing Campaign API built with Flask. The interview has two parts:

- **Part 1 (No AI):** Complete the CRUD endpoints in Flask
- **Part 2 (AI-assisted):** Convert the Flask API to FastAPI

## Quick Start

Download the provided zip file, unzip it, and open the directory in your editor.

### Option A: Docker (recommended)

```bash
docker compose up -d --build

# Enter the container — this is where you'll run pytest and the app
docker compose exec app bash
```

To start the Flask server (needed for manual curl testing):

```bash
# Inside the container
python app.py
```

The API will be available at http://localhost:5050.

> **Note:** Use `docker compose exec`, not `docker compose run`. `run` creates a
> temporary container that exits when the command finishes; `exec` runs inside the
> already-running container, which stays up regardless of exit codes.
>
> **Tip:** pytest uses Flask's in-process test client and does not require the server
> to be running. You can run `pytest tests/ -v` directly without starting `python app.py`.

### Option B: Local (no Docker)

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python app.py
```

The API will be available at http://localhost:5050.

## Current State

The API has the following endpoints:

| Method | Endpoint | Status |
|--------|----------|--------|
| GET | `/health` | ✅ Implemented |
| GET | `/campaigns` | ✅ Implemented |
| POST | `/campaigns` | ✅ Implemented |
| GET | `/campaigns/<id>` | ✅ Implemented |
| PATCH | `/campaigns/<id>` | ❌ Not implemented |
| DELETE | `/campaigns/<id>` | ❌ Not implemented |

Sample data is pre-seeded when you start the application.

---

## Part 1: Complete the CRUD Operations (15-20 min)

**No AI tools for this part.** Read the existing code and implement the missing endpoints.

### 1. Implement PATCH `/campaigns/<id>` — Update an existing campaign

- Accept partial updates (only update fields that are provided)
- Return 404 if campaign not found
- Validate `parent_campaign_id` if provided
- Return the updated campaign

### 2. Implement DELETE `/campaigns/<id>` — Delete a campaign

- Return 404 if campaign not found
- Consider: what should happen to sub-campaigns of this campaign?
- Return appropriate success response

### Testing Part 1

```bash
# Option A: run from inside the container (docker compose exec app bash)
# Option B: run directly in your activated venv

# Run the test suite
pytest tests/ -v

# Or test manually with curl
curl http://localhost:5050/campaigns

curl -X PATCH http://localhost:5050/campaigns/camp-002 \
  -H "Content-Type: application/json" \
  -d '{"goal": "Convert 10% of trial signups to paid"}'

curl -X DELETE http://localhost:5050/campaigns/camp-005
```

---

## Part 2: Convert to FastAPI (15-20 min)

**AI tools are encouraged for this part.** Using your completed Flask API as a reference, create a new FastAPI version.

### What to do

1. Create a new file `app_fastapi.py`
2. Migrate all endpoints from Flask to FastAPI
3. Use FastAPI idioms (Pydantic models, type hints, path parameters)
4. Run it with: `uvicorn app_fastapi:app --host 0.0.0.0 --port 8000 --reload`

### FastAPI Quick Reference

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None

@app.get("/items/{item_id}")
def get_item(item_id: str):
    ...

@app.post("/items", status_code=201)
def create_item(item: Item):
    ...
```

### Key differences from Flask

| Flask | FastAPI |
|-------|---------|
| `@app.route('/path', methods=['GET'])` | `@app.get('/path')` |
| `request.get_json()` | Pydantic model as parameter |
| `jsonify(data), 404` | `raise HTTPException(status_code=404)` |
| `request.args.get('key')` | `def endpoint(key: str = None)` |
| `dataclass` for models | `pydantic.BaseModel` for models |

### Testing Part 2

```bash
# Run FastAPI (port 8000)
uvicorn app_fastapi:app --host 0.0.0.0 --port 8000 --reload

# Test endpoints
curl http://localhost:8000/campaigns
curl http://localhost:8000/campaigns/camp-001
```

---

## Time Allocation

| Phase | Duration |
|-------|----------|
| Environment setup & code review | 5 min |
| Part 1: Flask CRUD implementation | 15-20 min |
| Part 2: FastAPI conversion | 15-20 min |
| Discussion | 5 min |
