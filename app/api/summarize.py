from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db_session import get_db
from app.core.security import get_current_user
from app.models.note import Note
from app.ml.summarizer import summarize_text


router = APIRouter()

@router.post("/{note_id}")
def summarize_note(note_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    note = db.query(Note).filter(Note.id == note_id, Note.owner_id == user.id).first()
    if not note:
        return {"error": "Note not found"}

    summary = summarize_text(note.content)
    note.summary = summary
    db.commit()
    db.refresh(note)

    return {"summary": summary}

