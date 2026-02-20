# 🎙️ Hindi Offline Voice Assistant  
### Vosk + Qwen 2.5 (1.5B) + Piper TTS

An intelligent **offline Hindi Voice Assistant** built using open-source speech recognition, a local Large Language Model (LLM), and neural text-to-speech synthesis.

This system listens to Hindi speech, processes it using a locally running AI model, and responds back in natural Hindi voice — completely offline after the initial setup.

---

## 📌 Overview

This project demonstrates real-time:

- 🎤 Speech-to-Text (Hindi)
- 🧠 Local LLM-based AI Processing
- 🔊 Neural Text-to-Speech
- 🔁 Continuous Voice Interaction Loop
- 🌐 Fully Offline AI System

It is ideal for:
- Edge AI deployment
- Raspberry Pi projects
- AI Voice Interface development
- Academic and research purposes

---

## 🚀 Features

- 🎤 Hindi Speech Recognition (Offline)
- 🧠 AI Responses using Qwen 2.5 (1.5B)
- 🔊 Natural Hindi Voice Output
- 🌐 Fully Local Processing (No Cloud Required)
- ⚡ Lightweight & Efficient Architecture
- 🔁 Continuous Listening Mode
- 🧩 Modular Design

---

## 🏗️ System Architecture

```
User Speech (Hindi)
        ↓
Vosk (Speech → Text)
        ↓
Qwen 2.5 via Ollama (Text → AI Response)
        ↓
Piper TTS (Text → Speech)
        ↓
Audio Playback
```

---

## 🛠️ Technologies Used

| Component | Technology |
|------------|------------|
| Programming Language | Python |
| Speech Recognition | Vosk (Hindi Model) |
| Language Model | Qwen 2.5:1.5B |
| LLM Runtime | Ollama |
| Text-to-Speech | Piper |
| Audio Handling | PyAudio |
| Audio Playback | Pydub |

---

## 📦 Installation Guide

### 🔹 1. Install Python (3.8+)

Verify:

```bash
python --version
```

---

### 🔹 2. Install Python Dependencies

```bash
pip install vosk pyaudio pydub requests
```

If PyAudio fails:

**Ubuntu:**
```bash
sudo apt install portaudio19-dev
```

**Windows:**
Install precompiled PyAudio wheel.

---

### 🔹 3. Install Ollama (For Qwen Model)

Download from:

https://ollama.com

Pull Qwen model:

```bash
ollama pull qwen2.5:1.5b
```

Start Ollama server:

```bash
ollama serve
```

Verify model works:

```bash
ollama run qwen2.5:1.5b
```

---

### 🔹 4. Install Piper TTS

Download Piper binary from:

https://github.com/rhasspy/piper/releases

Ensure it works:

```bash
piper --help
```

If not, add Piper to your system PATH.

---

## 📁 Project Structure

```
Hindi-Voice-Assistant/
│
├── main.py
├── models/
│   ├── vosk-model-small-hi-0.22/
│   ├── hi_IN-rohan-medium.onnx
│   └── hi_IN-rohan-medium.onnx.json
│
└── README.md
```

Models are automatically downloaded during first execution.

---

## ▶️ Running the Application

```bash
python main.py
```

You should see:

```
✅ System Ready. Speak in Hindi...
```

Start speaking in Hindi 🎤

Press:

```
Ctrl + C
```

to stop the assistant.

---

## ⚙️ How It Works

### 1️⃣ Speech Recognition

- Microphone input captured via PyAudio
- Vosk converts Hindi speech to text
- Runs fully offline

### 2️⃣ AI Processing

- Text sent to Qwen 2.5 (1.5B)
- Model runs locally via Ollama
- System prompt ensures:
  - Hindi response
  - Concise answers
  - Helpful tone

### 3️⃣ Text-to-Speech

- Piper converts AI text response to speech
- Uses Hindi voice model: `hi_IN-rohan-medium`
- Generates temporary WAV file

### 4️⃣ Playback

- Audio played using Pydub
- File removed after playback
- Loop restarts for next input

---

## 🌐 Internet Requirement

Internet is required only for:

- First-time model downloads
- Pulling Qwen model via Ollama

After setup, system works fully offline.

---

## 🔧 Customization

Modify assistant behavior inside:

```python
system_prompt = "You are a helpful assistant. Respond in Hindi. Keep the answer concise."
```

You can change:

- Language
- Tone
- Formality
- Answer length
- Personality

---

## ⚠️ Troubleshooting

### ❌ Piper Not Found

Ensure:

```bash
piper --help
```

works in terminal.

---

### ❌ Ollama Connection Error

Ensure Ollama is running:

```bash
ollama serve
```

---

### ❌ Microphone Not Working

Check:

- Default audio input device
- Microphone permissions
- PyAudio installation

---

## 📌 Future Improvements

- Wake-word detection
- Conversation memory
- Noise cancellation
- Multi-language support
- GUI interface
- Raspberry Pi optimization
- Model fine-tuning
- Edge deployment optimization

---

## 🎓 Educational Value

This project demonstrates:

- Edge AI deployment
- Speech interface engineering
- Local LLM integration
- Real-time audio processing
- Offline AI assistant architecture
- End-to-end AI pipeline implementation

---

## 👨‍💻 Author

**Sridhar S**  
VLSI Student  
Chennai Institute of Technology  

---

## 📜 License

Open-source for educational and research purposes.

---

## ⭐ If You Like This Project

Consider:

- Giving a ⭐ on GitHub
- Forking and improving it
- Deploying on Raspberry Pi
- Adding wake-word support
- Extending to multi-language AI assistant

---

### 🔥 End of README
