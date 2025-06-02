from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
import whisper
from TTS.api import TTS
import sqlite3
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS middleware should be added immediately after app creation
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Whisper model (small for demo)
whisper_model = whisper.load_model("small")
# Load Coqui TTS model (modern VITS model for better quality)
tts = TTS(model_name="tts_models/en/vctk/vits")

DB_PATH = "conversations.db"

# Ensure DB exists
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_audio TEXT,
        user_text TEXT,
        ai_text TEXT,
        ai_audio TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

init_db()

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    audio_path = f"temp_{file.filename}"
    with open(audio_path, "wb") as f:
        f.write(await file.read())
    result = whisper_model.transcribe(audio_path)
    os.remove(audio_path)
    return {"text": result["text"]}

@app.post("/chat/")
async def chat(text: str = Form(...)):
    import requests
    try:
        # Format prompt for Llama-2-Chat style models
        prompt = text.strip()
        if not prompt.startswith("<s>"):
            prompt = f"<s> {prompt}"
        resp = requests.post(
            "http://llama:8001/completion",
            json={
                "prompt": prompt,
                "n_predict": 32,
                "stream": False,
                "stop": ["</s>"]  # Add stop token for cleaner output
            },
            timeout=30
        )
        resp.raise_for_status()
        data = resp.json()
        ai_text = data.get("content") or data.get("text") or str(data)
        # Post-process: remove leading/trailing whitespace and any stop token
        ai_text = ai_text.strip().replace("</s>", "").strip()
        print(f"Llama server response: {data}")
    except Exception as e:
        print(f"Error contacting Llama server: {e}")
        ai_text = "Sorry, the AI model is not available."
    return {"ai_text": ai_text}

@app.post("/tts/")
async def tts_endpoint(text: str = Form(...)):
    wav_path = "ai_response.wav"
    # Specify a default speaker for the multi-speaker model
    tts.tts_to_file(text=text, file_path=wav_path, speaker="p225")
    return FileResponse(wav_path, media_type="audio/wav", filename=wav_path)

@app.post("/log/")
async def log_conversation(user_audio: str = Form(...), user_text: str = Form(...), ai_text: str = Form(...), ai_audio: str = Form(...)):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO conversations (user_audio, user_text, ai_text, ai_audio) VALUES (?, ?, ?, ?)",
              (user_audio, user_text, ai_text, ai_audio))
    conn.commit()
    conn.close()
    return {"status": "ok"}

@app.get("/logs/")
async def get_logs():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM conversations ORDER BY timestamp DESC LIMIT 20")
    rows = c.fetchall()
    conn.close()
    return {"logs": rows}