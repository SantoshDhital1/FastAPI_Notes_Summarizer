from transformers import pipeline
from app.core.config import settings

summarizer_pipeline = pipeline("summarization", model=settings.SUMMARIZER_MODEL)
