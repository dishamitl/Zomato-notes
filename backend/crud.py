from sqlalchemy.orm import Session
import models
import schemas
from algorithms import (
    insertion_sort_by_key,
    binary_search_iterative,
    binary_search_recursive,
    linear_search,
)

# ---------- User CRUD ----------

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        name=user.name,
        email=user.email,
        password=user.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


# ---------- Note CRUD ----------

def create_note(db: Session, note: schemas.NoteCreate):
    db_note = models.Note(
        title=note.title,
        content=note.content,
        tag=note.tag,
        owner_id=note.owner_id
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def get_all_notes(db: Session):
    return db.query(models.Note).all()


def get_notes_by_tag(db: Session, tag: str):
    return db.query(models.Note).filter(models.Note.tag == tag).all()


def get_note_by_id(db: Session, note_id: int):
    return db.query(models.Note).filter(models.Note.id == note_id).first()


def update_note(db: Session, note_id: int, note: schemas.NoteUpdate):
    db_note = get_note_by_id(db, note_id)

    if not db_note:
        return None

    update_data = note.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_note, key, value)

    db.commit()
    db.refresh(db_note)
    return db_note


def delete_note(db: Session, note_id: int):
    db_note = get_note_by_id(db, note_id)

    if not db_note:
        return None

    db.delete(db_note)
    db.commit()
    return db_note
def bulk_create_notes(db: Session, notes: list[models.Note]):
    db.add_all(notes)
    db.commit()
    return notes

def search_notes(db, keyword=None, sort_by=None):
    if keyword is None and sort_by is None:
        return []

    notes = db.query(models.Note).filter(
    models.Note.tag == "kb-demo"
).all()

    result = []

    for note in notes:

        note_dict = {
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "tag": note.tag,
            "created_at": note.created_at
        }

        if keyword:

            score = note.content.lower().count(keyword.lower())
            if score == 0:
                continue

            note_dict["score"] = score

        if sort_by == "date":

            note_dict["created_at_epoch"] = note.created_at.timestamp()

        result.append(note_dict)

    if keyword:

        result = insertion_sort_by_key(result, "score")

    elif sort_by == "date":

        result = insertion_sort_by_key(result, "created_at_epoch")

    return result[:5]
def lookup_note(db, title: str, algo: str):

    notes = (
        db.query(models.Note)
        .order_by(models.Note.title.asc())
        .all()
    )

    titles = [note.title for note in notes]

    if algo == "iterative":

        index = binary_search_iterative(
            titles,
            title
        )

    elif algo == "recursive":

        index = binary_search_recursive(
            titles,
            title,
            0,
            len(titles) - 1
        )

    else:
        return None

    if index == -1:
        return None

    return notes[index]
def quick_find_note(db, tag: str):

    notes = db.query(models.Note).filter(
    models.Note.tag == tag
).all()

    note_list = []

    for note in notes:

        note_list.append(
            {
                "id": note.id,
                "title": note.title,
                "content": note.content,
                "tag": note.tag
            }
        )

    return linear_search(
        note_list,
        "tag",
        tag
    )
def get_ai_demo_notes(db):
    return (
        db.query(models.Note)
        .filter(models.Note.tag == "ai-demo")
        .all()
    )