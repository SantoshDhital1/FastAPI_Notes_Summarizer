from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.notes import NoteCreate, NoteOut, NoteUpdate
from app.models.note import Note
from app.database.db_session import get_db
from app.core.security import get_current_user
import crud

router = APIRouter()

# Endpoints
# Create a note
@router.post("/note", response_model=NoteOut)
def note_create(
    note: NoteCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
   return crud.create_note(note, db, user)

# Get all notes
@router.get("/note", response_model=list[NoteOut])
def get_notes(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Note).filter(Note.owner_id == user.id).all()

# Get specifi notes
@router.get("/note{note_id}", response_model=NoteOut)
def get_note(note_id, db: Session = Depends(get_db)):
    note = crud.get_note(db, note_id)
    if note is None:
        raise HTTPException(status_code=400, detail="Note not found.")
    return note

# Update note
@router.put("/note{note_id}", response_model=NoteOut)
def note_update(note_id, note = NoteUpdate, db:Session = Depends(get_db), user=Depends(get_current_user)):
    db_note = crud.update_note(note_id, note, db, user)
    if db_note is None:
        raise HTTPException(status_code=400, detail="Note not found.")
    return db_note

# Delete note
@router.delete("/note{note_id}", response_model=dict)
def note_delete(note_id, db: Session = Depends(get_db)):
    note = crud.delete_note(note_id, db)
    if note is None:
        raise HTTPException(status_code=400, detail="Note not found.")
    return {'detail':'Note deleted successfully.'}