from transformers import pipeline
from app.core.config import settings

# Lazy load the pipeline to avoid import-time errors
_summarizer_pipeline = None

def get_summarizer_pipeline():
    global _summarizer_pipeline
    if _summarizer_pipeline is None:
        # Use default model if not specified, or the specified model
        model = settings.SUMMARIZER_MODEL if settings.SUMMARIZER_MODEL else "facebook/bart-large-cnn"
        _summarizer_pipeline = pipeline("summarization", model=model)
    return _summarizer_pipeline

def summarize_text(text: str, max_length: int = None, min_length: int = None) -> str:
   
    if not text or len(text.strip()) < 50:
        return text.strip()  
    
    summarizer_pipeline = get_summarizer_pipeline()
    
    input_length = len(text.split()) 
    
    if input_length < 10:
        return text.strip()
    
    model_name = settings.SUMMARIZER_MODEL if settings.SUMMARIZER_MODEL else "facebook/bart-large-cnn"
    is_t5_model = "t5" in model_name.lower()
    
    input_text = f"summarize: {text}" if is_t5_model else text
    
    if max_length is None:
        
        max_length = min(max(int(input_length * 0.5), 20), 142)
    
    if min_length is None:
        min_length = min(max(int(input_length * 0.25), 5), max_length - 1)
    
    if min_length >= max_length:
        min_length = max(5, max_length - 1)
    
    try:
        result = summarizer_pipeline(
            input_text,
            max_length=max_length,
            min_length=min_length,
            do_sample=False,  
            truncation=True  
        )
        
        summary = result[0]["summary_text"]
        
        if summary.strip() == text.strip() or len(summary) >= len(text) * 0.9:
            # Try with more aggressive parameters
            new_max = max(int(input_length * 0.3), 15)
            new_min = max(int(input_length * 0.15), 5)
            if new_min < new_max:
                result = summarizer_pipeline(
                    input_text,
                    max_length=new_max,
                    min_length=new_min,
                    do_sample=False,
                    truncation=True
                )
                summary = result[0]["summary_text"]
        
        return summary.strip()
    except Exception as e:
        print(f"Summarization error: {e}")
        return text.strip()
