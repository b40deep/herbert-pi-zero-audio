from fastapi import FastAPI, UploadFile, File, HTTPException
import os
import uuid

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Root endpoint is working"}

@app.get("/{job_id}")
async def poll_status(job_id: str):
    return {"Job ID": f"Your Job ID is {job_id}"}

# Ensure the upload directory exists
os.makedirs("received_files", exist_ok=True)

@app.post("/")
async def upload_audio(file: UploadFile = File(...)):
    # Generate a unique filename for the received file
    filename = f"{uuid.uuid4().hex}.wav"
    filepath = f"received_files/{filename}"
    
    try:
        # 1. Save the uploaded file (chunked, in case the file is large)
        with open(filepath, "wb") as f:
            while chunk := await file.read(1024 * 1024):  # read 1 MB at a time
                f.write(chunk)
        print(f"SERVER:   Received file saved to {filepath}")

        # 2. STT processing
        intent:str = "This is a placeholder transcription result."  
        # intent = stt_service.get_text_from_audio(filepath)
        print(f"SERVER:   Transcription result: '{intent}'")

        # 3. LLM processing
        print("SERVER:   LLM request")
        llm_res:str = "This is a placeholder LLM response."
        # llm_res = llm_generate(prompt=intent)
        print(f"SERVER:   LLM result: '{llm_res}'")

        return {
            "status": "success", # later make this an Enum
            "filename": filename,
            "transcription": intent,
            "llm_response": llm_res,
        }

    except Exception as e:
        print(f"SERVER:   Error: {e}")
        # Optional: remove the partial file on error
        if os.path.exists(filepath):
            os.remove(filepath)
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="localhost", port=8000, reload=True)