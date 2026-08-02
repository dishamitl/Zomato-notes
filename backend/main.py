from fastapi import FastAPI, Depends, HTTPException, Header, BackgroundTasks, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy import text
from fastapi import Query
import time
from typing import Optional
import models
import schemas
import crud
from database import engine, get_db
from ai_service import get_ai_response, SYSTEM_PROMPT
import json
import logging
from semantic_search import semantic_search

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Zomato Notes API",
    description="Backend API for Zomato Notes Capstone Project",
    version="1.0"
)

# -------------------- CORS --------------------

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Middleware --------------------

class ProcessTimeMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time

        response.headers["X-Process-Time"] = str(round(process_time, 4))

        return response


app.add_middleware(ProcessTimeMiddleware)


@app.get("/")
def home():
    return {
        "message": "Welcome to Zomato Notes API"
    }
# -------------------- Authentication Dependency --------------------


API_TOKEN = "zomato123"

def verify_token(x_token: Optional[str] = Header(None)):
    if x_token is None:
        raise HTTPException(
            status_code=401,
            detail="Missing token."
        )

    if x_token != API_TOKEN:
        raise HTTPException(
            status_code=403,
            detail="Invalid token."
        )


def simulate_indexing(note_title: str):
    time.sleep(3)
    print(f"Note '{note_title}' indexed successfully.")
# -------------------- User Endpoints --------------------

@app.post("/users", response_model=schemas.UserResponse)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    return crud.create_user(db, user)
# -------------------- Note Endpoints --------------------

@app.post("/notes", response_model=schemas.NoteResponse)
def create_note(
    note: schemas.NoteCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Check whether owner exists
    owner = crud.get_user_by_id(db, note.owner_id)

    if owner is None:
        raise HTTPException(
            status_code=404,
            detail="Owner not found."
        )

    # Run background indexing
    background_tasks.add_task(
        simulate_indexing,
        note.title
    )
    created_note = crud.create_note(db, note)

    ai_suggestion = None

    try:
        ai_response = get_ai_response(
            created_note.content,
            SYSTEM_PROMPT
        )

        ai_suggestion = json.loads(ai_response)

    except Exception:
        logging.exception("Failed to parse AI response")
        ai_suggestion = None

    response = created_note.__dict__.copy()

    response["ai_suggestion"] = ai_suggestion

    return response

@app.get("/notes", response_model=list[schemas.NoteResponse])
def get_notes(
    tag: Optional[str] = None,
    db: Session = Depends(get_db)
):
    if tag:
        return crud.get_notes_by_tag(db, tag)

    return crud.get_all_notes(db)
@app.get("/notes/search")
def search_notes(
    keyword: str | None = None,
    sort_by: str | None = None,
    db: Session = Depends(get_db)
):

    return crud.search_notes(
        db,
        keyword,
        sort_by
    )
@app.get("/notes/lookup")
def lookup_note(
    title: str,
    algo: str,
    db: Session = Depends(get_db)
):

    note = crud.lookup_note(
        db,
        title,
        algo
    )

    if note is None:

        raise HTTPException(
            status_code=404,
            detail="Note not found."
        )

    return note
@app.get("/notes/quick-find")
def quick_find(
    tag: str,
    db: Session = Depends(get_db)
):

    note = crud.quick_find_note(
        db,
        tag
    )

    if note is None:

        raise HTTPException(
            status_code=404,
            detail="No note found."
        )

    return note
@app.get("/notes/smart-search")
def smart_search(
    q: str,
    db: Session = Depends(get_db)
):

    notes = crud.get_ai_demo_notes(db)

    note_list = []

    for note in notes:

        note_list.append({

            "id": note.id,
            "title": note.title,
            "content": note.content,
            "tag": note.tag,
            "owner_id": note.owner_id,
            "created_at": note.created_at

        })

    return semantic_search(q, note_list)
@app.get("/notes/{id}", response_model=schemas.NoteResponse)
def get_note(
    id: int,
    db: Session = Depends(get_db)
):
    note = crud.get_note_by_id(db, id)

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found."
        )

    return note
@app.put("/notes/{id}", response_model=schemas.NoteResponse)
def update_note(
    id: int,
    note: schemas.NoteUpdate,
    db: Session = Depends(get_db)
):
    updated_note = crud.update_note(db, id, note)

    if updated_note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found."
        )

    return updated_note
@app.delete("/notes/{id}")
def delete_note(
    id: int,
    db: Session = Depends(get_db),
    _: str = Depends(verify_token)
):
    deleted_note = crud.delete_note(db, id)

    if deleted_note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found."
        )

    return {
        "message": "Note deleted successfully."
    }
@app.post("/notes/import")
async def import_notes(
    owner_id: int = Query(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Validate owner
    owner = crud.get_user_by_id(db, owner_id)

    if owner is None:
        raise HTTPException(
            status_code=404,
            detail="Owner not found."
        )

    # Validate file type
    if not file.filename.endswith(".txt"):
        raise HTTPException(
            status_code=400,
            detail="Only .txt files are allowed."
        )

    content = await file.read()
    lines = content.decode("utf-8").splitlines()

    notes = []

    for line in lines:
        line = line.strip()

        if line:
            notes.append(
                models.Note(
                    title=line[:120],
                    content=line,
                    tag="imported",
                    owner_id=owner_id
                )
            )

    crud.bulk_create_notes(db, notes)

    return {
        "message": f"{len(notes)} notes imported successfully."
    }
@app.get("/reports/tag-summary")
def tag_summary(db: Session = Depends(get_db)):

    query = text("""
        SELECT tag, COUNT(*) AS note_count
        FROM notes
        GROUP BY tag
        HAVING COUNT(*) > 1
    """)

    result = db.execute(query)

    return [
        {
            "tag": row.tag,
            "note_count": row.note_count
        }
        for row in result
    ]
@app.get("/reports/long-notes")
def long_notes(db: Session = Depends(get_db)):

    query = text("""
        SELECT *
        FROM notes
        WHERE LENGTH(content) >
        (
            SELECT AVG(LENGTH(content))
            FROM notes
        )
    """)

    result = db.execute(query)

    return [
        dict(row._mapping)
        for row in result
    ]
@app.get("/reports/user-notes")
def user_notes(db: Session = Depends(get_db)):

    query = text("""
        SELECT
            users.id,
            users.name,
            COUNT(notes.id) AS total_notes
        FROM users
        LEFT JOIN notes
            ON users.id = notes.owner_id
        GROUP BY users.id, users.name
    """)

    result = db.execute(query)

    return [
        dict(row._mapping)
        for row in result
    ]
