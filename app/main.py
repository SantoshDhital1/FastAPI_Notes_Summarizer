from fastapi import FastAPI
from app.api import auth, notes, summarize
from app.database.db_session import engine
from app.database import base

base.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Notes Summarizer")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(notes.router, prefix="/notes", tags=["Notes"])
app.include_router(summarize.router, prefix="/summarize", tags=["Summarization"])

@app.get("/")
def root():
    return {"message": "Notes Summarizer API running"}
