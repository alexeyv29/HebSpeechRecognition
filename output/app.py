import os
import tempfile
import traceback
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai

app = FastAPI(title="Voice to Text - Hebrew Speech Recognition API")

# Enable CORS (useful if serving from different origins in development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """
    Serves the single-file HTML frontend.
    """
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Frontend HTML file not found.")

@app.post("/api/transcribe")
async def transcribe_audio(
    api_key: str = Form(...),
    audio_file: UploadFile = File(...)
):
    """
    Receives an audio file and api_key, sends it to Gemini 1.5 flash,
    and returns the transcribed Hebrew text.
    """
    if not api_key:
        raise HTTPException(status_code=400, detail="Gemini API key is required.")
        
    temp_audio_path = ""
    gemini_file = None

    try:
        # Secure the file handling using tempfile
        suffix = os.path.splitext(audio_file.filename)[1]
        if not suffix:
            suffix = ".mp3"  # default fallback
            
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_audio:
            content = await audio_file.read()
            temp_audio.write(content)
            temp_audio_path = temp_audio.name

        # Configure Gemini API
        genai.configure(api_key=api_key)

        # Upload file to Gemini GenAI API
        gemini_file = genai.upload_file(path=temp_audio_path, display_name=audio_file.filename)

        import asyncio
        # Wait until the file is active. Audio files require processing by Google before transcription
        while gemini_file.state.name == "PROCESSING":
            await asyncio.sleep(2)
            gemini_file = genai.get_file(gemini_file.name)
            
        if gemini_file.state.name == "FAILED":
            raise Exception("Gemini API failed to process the uploaded audio file.")

        # Dynamically discover the correct Flash model to avoid 404s
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        if 'models/gemini-1.5-flash' in available_models:
            model_id = 'models/gemini-1.5-flash'
        elif 'models/gemini-1.5-flash-latest' in available_models:
            model_id = 'models/gemini-1.5-flash-latest'
        elif 'models/gemini-1.5-flash-8b' in available_models:
            model_id = 'models/gemini-1.5-flash-8b'
        else:
            flash_models = [m for m in available_models if 'flash' in m.lower()]
            if flash_models:
                model_id = flash_models[0]
            elif available_models:
                model_id = available_models[0]
            else:
                model_id = 'models/gemini-1.5-flash'
                
        model = genai.GenerativeModel(model_id)
        
        # Prompt instructing to transcribe accurately with speaker diarization in Hebrew
        prompt = (
            "Please transcribe the speech in this audio exactly as it is spoken. "
            "The language is Hebrew. "
            "Separate the transcription by speakers and label each speaker (e.g., 'דובר 1:', 'דובר 2:' or their names if mentioned) so it reads like a real chat format. "
            "Return ONLY the transcribed text without any markdown formatting, headers, or extra commentary."
        )

        response = model.generate_content([prompt, gemini_file])

        # Return successfully mapped transcription
        return {"transcription": response.text.strip()}

    except Exception as e:
        # Avoid exposing raw sensitive errors directly but log if necessary
        error_msg = str(e)
        if "API_KEY_INVALID" in error_msg:
            detail = "Invalid Gemini API Key provided."
        else:
            detail = f"Transcription failed: {error_msg}"
        raise HTTPException(status_code=500, detail=detail)

    finally:
        # Cleanup GenAI uploaded file
        if gemini_file:
            try:
                genai.delete_file(gemini_file.name)
            except Exception:
                pass  # Suppress cleanup errors

        # Cleanup local temporary file
        if temp_audio_path and os.path.exists(temp_audio_path):
            try:
                os.remove(temp_audio_path)
            except Exception:
                pass

if __name__ == "__main__":
    import uvicorn
    # Start the server locally on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
