from fastapi import Depends
from app.database.db_session import get_db
from sqlalchemy.orm import session
from app.schemas.notes import NoteCreate, NoteOut, NoteUpdate
from app.models.note import Note
from app.core.security import get_current_user


def get_note(note_id: int, db:session = Depends(get_db), user = Depends(get_current_user)):
    return (
        db.query(Note).filter(Note.id == note_id).first()
    )

def create_note(note: NoteCreate, db:session = Depends(get_db), user = Depends(get_current_user)):
    new_note = Note(
        title = note.title,
        content = note.content,
        owner_id = user.id
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


def update_note(note_id: int, note = NoteUpdate, db:session = Depends(get_db), user = Depends(get_current_user)):
    db_note = db.query(Note).filter(Note.id == note_id, Note.owner_id == user.id).first()
    if db_note:
        db_note.title = note.title
        db_note.content = note.content
        db.commit()
        db.refresh(db_note)

    return db_note

def delete_note(note_id: int, db:session = Depends(get_db)):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if db_note:
        db.delete(db_note)
        db.commit()
    return db_note