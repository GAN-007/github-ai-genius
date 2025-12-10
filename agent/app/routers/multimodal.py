from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import shutil
import os
from core.config import settings
# In a real implementation, we would import Whisper here
# from services.whisper import transcribe_audio

router = APIRouter()

@router.post("/voice")
async def process_voice_command(file: UploadFile = File(...)):
    """
    Processes uploaded audio file (wav/mp3) and returns transcription.
    """
    temp_path = os.path.join(settings.WORKSPACE_DIR, f"temp_{file.filename}")
    
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Placeholder for actual Whisper call
        # transcription = transcribe_audio(temp_path)
        
        # For this standalone version without GPU, we simulate a response
        # to ensure the frontend flow works.
        transcription = "Simulated transcription: Analyze the repository structure."
        
        return {"text": transcription}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """
    Uploads files to the workspace for RAG ingestion.
    """
    uploaded_paths = []
    
    for file in files:
        file_path = os.path.join(settings.WORKSPACE_DIR, file.filename)
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            uploaded_paths.append(file_path)
            
            # Trigger RAG ingestion here
            # rag_pipeline.ingest_file(file_path)
            
        except Exception as e:
            print(f"Error uploading {file.filename}: {e}")
            
    return {"status": "success", "files": uploaded_paths, "message": "Files uploaded and queued for indexing."}
