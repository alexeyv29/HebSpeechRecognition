# HebSpeechRecognition - Hebrew Voice-to-Text with Gemini AI

HebSpeechRecognition is a modern, high-performance web application designed to natively transcribe Hebrew audio and video files. It leverages Google's state-of-the-art **Gemini 1.5 Flash** Generative Model to provide highly accurate transcriptions, featuring built-in speaker diarization.

## 🚀 Features
- **Premium Frontend:** A beautiful, responsive, mobile-first dark theme UI wrapped into an ultra-clean, single-file HTML frontend.
- **Asynchronous Audio Handling:** Effortlessly handles large audio files natively, correctly waiting for Gemini Cloud Processing to reach an `ACTIVE` state.
- **Hebrew Native Support:** Correctly formatted Right-To-Left (RTL) output while maintaining proper cross-platform layouts.
- **Speaker Diarization:** Automatically separates the transcription by different voices so it reads clearly like a human chat transcript (e.g., `דובר 1:`, `דובר 2:`).
- **Dynamic Model Discovery:** Specifically scans your `API Key` authorizations via HTTP to guarantee it binds to your exact supported Gemini Flash Node version.

## 🛠️ Technical Stack
- **Backend:** [FastAPI](https://fastapi.tiangolo.com/) & Uvicorn (Python 3)
- **AI Model Client:** Google Gen AI (`google-generativeai` SDK)
- **Frontend Design:** Pure HTML5, CSS3 Variables, Vanilla JS (Zero build-steps)
- **Typography:** Google Fonts (Heebo, Inter)

## 📋 Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd HebSpeechRecognition
   ```

2. **Initialize your Python Virtual Environment:**
   Run the following commands in your terminal to create and activate a secluded virtual environment to avoid global conflicts.
   
   *Windows:*
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
   
   *Mac/Linux:*
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the FastAPI Server:**
   ```bash
   python app.py
   ```

5. **Start Transcribing:**
   Open your browser and navigate to `http://localhost:8000`. You will need your own active Google Gemini API key to authorize the AI processing.
