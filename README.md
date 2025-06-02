# AI Voice Agent Demo

This is a demo system using FastAPI, Whisper, Llama.cpp, Coqui TTS, SQLite, and a simple HTML/JS frontend. All components are orchestrated with Docker Compose.

## Components
- **backend/**: FastAPI app (Python, Poetry) for audio transcription, LLM chat, TTS, and logging
- **frontend/**: Simple HTML + JS UI for audio input/output and conversation log
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

## 🧠 Downloading Required AI Models

**Note:** The models are not included in the repository due to their large size and licensing restrictions. Please follow the steps below to download and place the models in the correct directories.

---

### 1. Llama-2-7B-Chat Model (GGUF or GGML)

- **GGUF Format (Recommended for llama.cpp v2+):**
  - Download from:  
    [TheBloke/Llama-2-7B-Chat-GGUF on Hugging Face](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF)
  - Example file: `llama-2-7b-chat.Q4_K_M.gguf`
  - Place the downloaded file in the `models/` directory:
    ```
    models/llama-2-7b-chat.gguf
    ```

- **GGML Format (Legacy, if needed):**
  - Download from:  
    [TheBloke/Llama-2-7B-Chat-GGML on Hugging Face](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML)
  - Example file: `llama-2-7b-chat.ggmlv3.q4_0.bin`
  - Place the downloaded file in the `models/` directory:
    ```
    models/llama-2-7b-chat.ggmlv3.q4_0.bin
    ```

---

### 2. Whisper Model (for Speech-to-Text)

- The backend uses the `small` Whisper model, which will be automatically downloaded by the `whisper` Python package on first run.  
  No manual action is needed.

---

### 3. Coqui TTS Model

- The backend uses the `tts_models/en/vctk/vits` model, which will be automatically downloaded by the TTS library on first run.  
  No manual action is needed.

---

## 📥 Example: Downloading a Llama-2 Model

1. Go to the [Hugging Face Llama-2-7B-Chat-GGUF page](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF).
2. Download your preferred quantized file (e.g., `llama-2-7b-chat.Q4_K_M.gguf`).
3. Place it in the `models/` directory of this project.
4. Update your Docker Compose or server command if the filename is different.

---

## 🛠️ Downloading and Building llama.cpp

This project uses [llama.cpp](https://github.com/ggerganov/llama.cpp) for running the Llama-2 model. To set it up:

1. **Clone llama.cpp:**
   ```bash
   git clone https://github.com/ggerganov/llama.cpp.git
   cd llama.cpp
   ```
2. **(Optional) Checkout a specific version:**
   ```bash
   git checkout <tag-or-commit>
   ```
3. **Copy the following Dockerfile into `llama.cpp/Dockerfile`:**

   ```dockerfile
   # syntax=docker/dockerfile:1
   FROM ubuntu:22.04

   RUN apt-get update && \
       apt-get install -y --no-install-recommends \
           build-essential \
           cmake \
           python3 \
           python3-pip \
           git \
           curl \
           ca-certificates \
           libopenblas-dev \
           libssl-dev \
           libcurl4-openssl-dev \
           wget \
           && rm -rf /var/lib/apt/lists/*

   WORKDIR /app
   COPY . /app

   RUN cmake -B build -S . -DLLAMA_BUILD_SERVER=ON && \
       cmake --build build --target llama-server -j

   EXPOSE 8001

   CMD ["/app/build/bin/llama-server", "-m", "/models/llama-2-7b-chat.ggmlv3.q4_0.bin", "--host", "0.0.0.0", "--port", "8001"]
   ```

4. **Build the Docker image and run the server as described in the main README.**

---
