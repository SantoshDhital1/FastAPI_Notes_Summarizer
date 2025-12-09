from app.database.db_session import get_db
from sqlalchemy.orm import Session
from app.schemas.notes import NoteCreate, NoteOut, NoteUpdate
from app.models.note import Note
from app.models.user import User


def get_note(note_id: int, db: Session):
    return (
        db.query(Note).filter(Note.id == note_id).first()
    )

def create_note(note: NoteCreate, db: Session, user: User):
    new_note = Note(
        title = note.title,
        content = note.content,
        owner_id = user.id
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


def update_note(note_id: int, note: NoteUpdate, db: Session, user: User):
    db_note = db.query(Note).filter(Note.id == note_id, Note.owner_id == user.id).first()
    if db_note:
        if note.title is not None:
            db_note.title = note.title
        if note.content is not None:
            db_note.content = note.content
        db.commit()
        db.refresh(db_note)

    return db_note

def delete_note(note_id: int, db: Session):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if db_note:
        db.delete(db_note)
        db.commit()
    return db_note