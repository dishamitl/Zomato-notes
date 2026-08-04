# Zomato Notes

A full-stack Notes Management application built using **FastAPI**, **SQLAlchemy**, **SQLite**, **HTML**, **CSS**, and **Vanilla JavaScript**. The project demonstrates REST API development, frontend integration, algorithm implementation, semantic search, AI-powered note suggestions, and database operations.

---

# Tech Stack

## Backend
- FastAPI
- SQLAlchemy ORM
- SQLite
- Pydantic
- Python

## Frontend
- HTML5
- CSS3
- Vanilla JavaScript

## AI & Machine Learning
- Sentence Transformers
- all-MiniLM-L6-v2
- scikit-learn (Cosine Similarity)
- Mock AI Mode
- python-dotenv

---

# Project Structure

```
zomato-notes/
│
├── backend/
│   ├── main.py
│   ├── crud.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── algorithms.py
│   ├── ai_service.py
│   ├── semantic_search.py
│   ├── ranking_dataset.py
│   ├── ai_sample_notes.py
│   ├── seed.py
│   ├── .env.example
│   └── sample_import.txt
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/dishamitl/Zomato-notes.git
cd zomato-notes
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```
---

## Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file inside the **backend** folder.

```
MOCK_AI=1
```

Mock mode generates AI suggestions locally without requiring an external API key.

---

## Seed the Database

```bash
cd backend
python seed.py
```

---

## Run Backend

```bash
uvicorn main:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

---

## Run Frontend

Open the **frontend** folder using **Live Server** in VS Code.

Frontend runs at:

```
http://127.0.0.1:5500
```

---

# Features

## User Management

- Create users
- Owner validation

## Notes Management

- Create notes
- View all notes
- Update notes
- Delete notes
- Filter notes by tag

## Validation

- Pydantic validation
- Error handling
- Owner existence validation

## Background Tasks

- Simulated note indexing after note creation

## Middleware

- Request processing time middleware

## File Upload

- Bulk import notes from a `.txt` file

## SQL Reports

- Tag summary report
- Long notes report
- User notes report

---

# API Endpoints

## Users

| Method | Endpoint |
|---------|----------|
| POST | /users |

---

## Notes

| Method | Endpoint |
|---------|----------|
| POST | /notes |
| GET | /notes |
| GET | /notes/{id} |
| PUT | /notes/{id} |
| DELETE | /notes/{id} |

---

## Search & Algorithms

| Method | Endpoint |
|---------|----------|
| GET | /notes/search |
| GET | /notes/lookup |
| GET | /notes/quick-find |
| GET | /notes/smart-search |

---

## Import

| Method | Endpoint |
|---------|----------|
| POST | /notes/import |

---

## Reports

| Method | Endpoint |
|---------|----------|
| GET | /reports/tag-summary |
| GET | /reports/long-notes |
| GET | /reports/user-notes |

---

# Authentication

Deleting notes requires an authentication header.

```
x-token: zomato123
```

---

# Part 2 – Algorithms

The project manually implements the following algorithms without using:

- `sorted()`
- `list.sort()`

## Insertion Sort

Used for:

- Keyword relevance ranking
- Date sorting

Endpoint:

```
GET /notes/search
```

Example:

```
/notes/search?keyword=apple

/notes/search?sort_by=date
```

---

## Iterative Binary Search

Endpoint:

```
GET /notes/lookup
```

Example:

```
/notes/lookup?title=Apple Harvest Notes&algo=iterative
```

---

## Recursive Binary Search

Example:

```
/notes/lookup?title=Apple Harvest Notes&algo=recursive
```

---

## Linear Search

Endpoint:

```
GET /notes/quick-find
```

Example:

```
/notes/quick-find?tag=work
```

---

# Part 3 – AI Features

## AI Note Suggestions

Whenever a new note is created:

- AI generates suggested tags
- AI generates a short summary
- Suggestions are returned in the API response

Example:

```json
{
  "ai_suggestion": {
    "tags": [
      "backend",
      "api"
    ],
    "summary": "Discussed backend API integration."
  }
}
```

---

## Smart Search

Semantic search is powered by the **Sentence Transformers** model **all-MiniLM-L6-v2**.

The query and notes are converted into embeddings, cosine similarity is calculated, and the three most relevant notes are returned.

Endpoint:

```
GET /notes/smart-search?q=workout
```

Response includes similarity scores.

---

## Mock AI Mode

AI suggestions are generated locally using:

```
MOCK_AI=1
```

No external API key is required.

---

## Prompt Engineering

The AI prompt follows a structured template including:

- Instructions
- Context
- Input
- Constraints
- Output Format

The AI returns only valid JSON.

---

# Frontend Features

- Responsive interface
- Create notes
- Delete notes
- Filter notes
- Keyword search
- Sort by relevance
- Sort by date
- Exact title lookup
- Quick tag search
- Semantic smart search
- AI suggestion panel
- Apply AI-generated tag
- Category tree navigation
- Highlight matched notes

---

# Algorithms Used

- Insertion Sort
- Iterative Binary Search
- Recursive Binary Search
- Linear Search
- Sentence Embeddings
- Cosine Similarity

---

# Database

SQLite database seeded with:

- Sample users
- Sample notes
- Ranking dataset
- AI sample dataset

---

# Sample Import File

The repository includes:

```
sample_import.txt
```

This file can be used to test the bulk import endpoint.

---

# License

This project was created for educational purposes as part of the **Zomato Backend Capstone Assignment**.

---

# Author

**Disha Mittal**
iitp_sdai_26021397