from sqlalchemy.orm import Session
import models
import schemas


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