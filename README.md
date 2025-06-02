# AI Voice Agent Demo

This is a demo system using FastAPI, Whisper, Llama.cpp, Coqui TTS, SQLite, and a simple HTML/JS frontend. All components are orchestrated with Docker Compose.

## Components
- **backend/**: FastAPI app (Python, Poetry) for audio transcription, LLM chat, TTS, and logging
- **frontend/**: Simple HTML/JS UI for audio input/output and conversation log
- **llama.cpp**: Open-source LLM running in a Docker container

## Quick Start

1. Place your Llama.cpp model in `./models/` (e.g., `llama-2-7b-chat.ggmlv3.q4_0.bin`).
2. Build and start all services:

```sh
docker-compose up --build
```

3. Open the frontend:
- If running locally, visit [http://localhost:8000](http://localhost:8000)

## Endpoints
- `/transcribe/` (POST): Audio upload → transcription
- `/chat/` (POST): Text → Llama.cpp response
- `/tts/` (POST): Text → speech audio
- `/log/` (POST): Log conversation
- `/logs/` (GET): Get recent logs

## Notes
- All models run locally, no cloud APIs required.
- For demo, audio files are not persisted in logs.
- Llama.cpp model must be downloaded separately.

## License
Open source, demo only.
