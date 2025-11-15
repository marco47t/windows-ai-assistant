# 🤖 Windows AI Assistant

> A modern, powerful desktop AI assistant for Windows featuring voice interaction, intelligent chat, and seamless system control.

![Status](https://img.shields.io/badge/status-in%20development-yellow)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![React](https://img.shields.io/badge/react-19-61dafb)
![Electron](https://img.shields.io/badge/electron-latest-47848f)

## ✨ Features

### 🗣️ Voice Interaction
- Wake word detection ("Hey Assistant")
- Real-time speech-to-text conversion
- Natural text-to-speech responses
- Multi-language support
- Noise cancellation

### 💬 Chat Interface
- Beautiful, modern UI with glassmorphic design
- Real-time messaging with AI
- Message history and context awareness
- Code syntax highlighting
- File attachment support
- Markdown rendering

### 🎮 System Control
- Application management (open/close apps)
- File system operations
- System settings control (volume, brightness, WiFi)
- Window management
- Screenshot capture
- Process monitoring

### 🧠 AI Capabilities
- Powered by Groq (Llama 3.1)
- Natural language understanding
- Context-aware responses
- Task automation
- Web search integration
- Code generation & explanation

## 🏗️ Architecture

```
Windows AI Assistant
├── Frontend (React + Electron)
│   ├── User Interface
│   ├── WebSocket Client
│   └── System Tray Integration
│
├── Backend (Python FastAPI)
│   ├── API Endpoints
│   ├── AI Logic (Groq)
│   ├── WebSocket Server
│   └── Database (SQLite)
│
└── Voice Service (Python)
    ├── Speech Recognition
    ├── Text-to-Speech
    └── Wake Word Detection
```

## 🚀 Getting Started

### Prerequisites
- Python 3.11 or higher
- Node.js 18 or higher
- Windows 10/11
- Groq API key

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/marco47t/windows-ai-assistant.git
cd windows-ai-assistant
```

2. **Set up the backend**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

3. **Set up the voice service**
```bash
cd ../voice-service
pip install -r requirements.txt
```

4. **Set up the frontend**
```bash
cd ../frontend
npm install
```

### Running the Application

1. **Start the backend** (Terminal 1)
```bash
cd backend
venv\Scripts\activate
python main.py
```

2. **Start the voice service** (Terminal 2)
```bash
cd voice-service
python voice_service.py
```

3. **Start the frontend** (Terminal 3)
```bash
cd frontend
npm start
```

## 📁 Project Structure

```
windows-ai-assistant/
├── frontend/               # React + Electron app
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/        # Main pages
│   │   ├── services/     # API services
│   │   ├── store/        # State management
│   │   └── styles/       # CSS/Tailwind
│   ├── public/
│   └── electron/         # Electron main process
│
├── backend/               # FastAPI server
│   ├── api/              # API endpoints
│   ├── models/           # Database models
│   ├── services/         # Business logic
│   ├── core/             # Core utilities
│   └── main.py           # Entry point
│
├── voice-service/         # Voice processing
│   ├── recognition/      # Speech-to-text
│   ├── synthesis/        # Text-to-speech
│   └── wake_word/        # Wake word detection
│
└── docs/                  # Documentation
```

## 🛠️ Tech Stack

### Frontend
- **React 19** - UI framework
- **TypeScript** - Type safety
- **Electron** - Desktop application
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **Zustand** - State management
- **WebSocket** - Real-time communication

### Backend
- **FastAPI** - Web framework
- **SQLite** - Database
- **Groq API** - AI model (Llama 3.1)
- **WebSocket** - Real-time communication
- **Pydantic** - Data validation

### Voice Service
- **SpeechRecognition** - Speech-to-text
- **pyttsx3** - Text-to-speech
- **PyAudio** - Audio processing
- **Porcupine** - Wake word detection

## 🗓️ Development Roadmap

- [x] Project setup and structure
- [ ] **Phase 1**: Foundation (Weeks 1-2)
  - [ ] Basic chat interface
  - [ ] WebSocket communication
  - [ ] Simple AI responses
- [ ] **Phase 2**: Voice Integration (Weeks 3-4)
  - [ ] Speech recognition
  - [ ] Text-to-speech
  - [ ] Wake word detection
- [ ] **Phase 3**: System Control (Weeks 5-6)
  - [ ] Application management
  - [ ] File operations
  - [ ] System settings
- [ ] **Phase 4**: Polish & Features (Weeks 7-8)
  - [ ] UI refinements
  - [ ] Performance optimization
  - [ ] Advanced AI features
- [ ] **Phase 5**: Distribution (Weeks 9-10)
  - [ ] Electron packaging
  - [ ] Installer creation
  - [ ] Documentation

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Groq for providing the AI API
- The open-source community for amazing tools

---

**Built with ❤️ by [marco47t](https://github.com/marco47t)**