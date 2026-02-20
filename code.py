import os
import sys
import json
import wave
import zipfile
import requests
import shutil
import subprocess
import pyaudio
from pydub import AudioSegment
from pydub.playback import play

# Try imports for core engines
try:
    import vosk
except ImportError:
    print("Vosk not found. Install with: pip install vosk")
    sys.exit(1)

# --- Configuration & Paths ---
MODELS_DIR = "models"
VOSK_MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-small-hi-0.22.zip"
VOSK_MODEL_NAME = "vosk-model-small-hi-0.22"
VOSK_MODEL_PATH = os.path.join(MODELS_DIR, VOSK_MODEL_NAME)

PIPER_MODEL_URL = "https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/hi_IN/rohan/medium/hi_IN-rohan-medium.onnx"
PIPER_CONFIG_URL = "https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/hi_IN/rohan/medium/hi_IN-rohan-medium.onnx.json"
PIPER_MODEL_FILE = os.path.join(MODELS_DIR, "hi_IN-rohan-medium.onnx")
PIPER_CONFIG_FILE = os.path.join(MODELS_DIR, "hi_IN-rohan-medium.onnx.json")

# --- Model Setup Functions ---

def ensure_models_dir():
    if not os.path.exists(MODELS_DIR):
        os.makedirs(MODELS_DIR)

def ensure_vosk_model():
    ensure_models_dir()
    if os.path.exists(VOSK_MODEL_PATH):
        return VOSK_MODEL_PATH
    print("Downloading Vosk model...")
    r = requests.get(VOSK_MODEL_URL, stream=True)
    zip_path = os.path.join(MODELS_DIR, "vosk.zip")
    with open(zip_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192): f.write(chunk)
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(MODELS_DIR)
    os.remove(zip_path)
    return VOSK_MODEL_PATH

def ensure_piper_model():
    ensure_models_dir()
    if not os.path.exists(PIPER_MODEL_FILE):
        print("Downloading Piper model...")
        r = requests.get(PIPER_MODEL_URL)
        with open(PIPER_MODEL_FILE, "wb") as f: f.write(r.content)
    if not os.path.exists(PIPER_CONFIG_FILE):
        r = requests.get(PIPER_CONFIG_URL)
        with open(PIPER_CONFIG_FILE, "wb") as f: f.write(r.content)
    return PIPER_MODEL_FILE, PIPER_CONFIG_FILE

# --- Core Logic Functions ---

def get_qwen_response(prompt):
    """Sends text to Ollama (Local Qwen 2.5 1.5B)"""
    url = "http://localhost:11434/api/generate"
    system_prompt = "You are a helpful assistant. Respond in Hindi. Keep the answer concise."
    # CHANGED: 'llama3.1' replaced with 'qwen2.5:1.5b'
    data = {"model": "qwen2.5:1.5b", "prompt": f"{system_prompt}\n\nUser: {prompt}", "stream": False}
    try:
        response = requests.post(url, json=data)
        return response.json().get('response', '').replace("उत्तर:", "").strip()
    except Exception as e:
        return "क्षमा करें, मैं अभी कनेक्ट नहीं हो पा रहा हूँ।"

def generate_audio_piper(text, output_file, model_file):
    """Converts text to speech using Piper binary"""
    piper_bin = shutil.which("piper") or os.path.join(os.path.dirname(sys.executable), "piper")
    if not piper_bin:
        print("Piper binary not found.")
        return False
    try:
        cmd = [piper_bin, "--model", model_file, "--output_file", output_file]
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        process.communicate(input=text.encode('utf-8'))
        return True
    except Exception as e:
        print(f"TTS Error: {e}")
        return False

# --- Main Interaction Loop ---

def main():
    # 1. Initialize
    vosk_path = ensure_vosk_model()
    piper_model, _ = ensure_piper_model()
    
    model = vosk.Model(vosk_path)
    rec = vosk.KaldiRecognizer(model, 16000)
    
    # Setup Mic
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    print("\n✅ System Ready. Speak in Hindi...")

    try:
        while True:
            # Step A: Listen
            data = stream.read(4000, exception_on_overflow=False)
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                user_text = result.get("text", "")

                if user_text.strip():
                    print(f"\n👤 You: {user_text}")

                    # Step B: Brain (Qwen)
                    print("🤖 Thinking...")
                    # CHANGED: Function call updated here
                    ai_response = get_qwen_response(user_text)
                    print(f"🤖 AI: {ai_response}")

                    # Step C: Voice (Piper)
                    output_wav = "response.wav"
                    if generate_audio_piper(ai_response, output_wav, piper_model):
                        # Step D: Play
                        audio_out = AudioSegment.from_wav(output_wav)
                        play(audio_out)
                        os.remove(output_wav)
                    
                    print("\n🎤 Listening again...")

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    main()