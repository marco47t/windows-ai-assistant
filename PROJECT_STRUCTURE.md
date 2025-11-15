# Project Structure Documentation

## Overview

This document details the architecture and organization of the Windows AI Assistant project.

## System Architecture

### Three-Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend Layer                           │
│         (React + Electron - User Interface)                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   Chat   │  │  Voice   │  │ Settings │  │  System  │   │
│  │    UI    │  │   Input  │  │    UI    │  │   Tray   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                         ↕ WebSocket
┌─────────────────────────────────────────────────────────────┐
│                      Backend Layer                           │
│           (Python FastAPI - API & Logic)                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │    API   │  │    AI    │  │ Database │  │WebSocket │   │
│  │ Endpoints│  │  Service │  │  SQLite  │  │  Server  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                         ↕ REST API
┌─────────────────────────────────────────────────────────────┐
│                   Voice Service Layer                        │
│          (Python - Speech Processing)                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │  Speech  │  │   Text   │  │   Wake   │                  │
│  │  to Text │  │to Speech │  │   Word   │                  │
│  └──────────┘  └──────────┘  └──────────┘                  │
└─────────────────────────────────────────────────────────────┘
```

## Directory Structure

### Frontend (`/frontend`)

```
frontend/
├── public/                 # Static assets
│   ├── index.html
│   └── icons/
│
├── src/
│   ├── components/        # Reusable React components
│   │   ├── Chat/
│   │   │   ├── ChatMessage.tsx
│   │   │   ├── ChatInput.tsx
│   │   │   └── ChatHistory.tsx
│   │   ├── Voice/
│   │   │   ├── VoiceButton.tsx
│   │   │   └── VoiceIndicator.tsx
│   │   └── Common/
│   │       ├── Button.tsx
│   │       ├── Input.tsx
│   │       └── Modal.tsx
│   │
│   ├── pages/            # Main application pages
│   │   ├── Home.tsx
│   │   ├── Chat.tsx
│   │   └── Settings.tsx
│   │
│   ├── services/         # API and service integrations
│   │   ├── api.ts
│   │   ├── websocket.ts
│   │   └── storage.ts
│   │
│   ├── store/           # State management (Zustand)
│   │   ├── chatStore.ts
│   │   ├── settingsStore.ts
│   │   └── voiceStore.ts
│   │
│   ├── styles/          # Global styles
│   │   ├── globals.css
│   │   └── themes.css
│   │
│   ├── types/           # TypeScript type definitions
│   │   ├── chat.ts
│   │   └── api.ts
│   │
│   ├── utils/           # Utility functions
│   │   ├── formatters.ts
│   │   └── validators.ts
│   │
│   ├── App.tsx          # Main React component
│   └── index.tsx        # Entry point
│
├── electron/            # Electron main process
│   ├── main.js         # Electron entry point
│   ├── preload.js      # Preload script
│   └── tray.js         # System tray handler
│
├── package.json
├── tsconfig.json
└── tailwind.config.js
```

### Backend (`/backend`)

```
backend/
├── api/                    # API endpoints
│   ├── __init__.py
│   ├── chat.py            # Chat endpoints
│   ├── system.py          # System control endpoints
│   └── websocket.py       # WebSocket endpoints
│
├── models/                 # Database models
│   ├── __init__.py
│   ├── conversation.py
│   ├── message.py
│   └── settings.py
│
├── services/               # Business logic
│   ├── __init__.py
│   ├── ai_service.py      # AI/Groq integration
│   ├── system_service.py  # System control logic
│   └── chat_service.py    # Chat management
│
├── core/                   # Core utilities
│   ├── __init__.py
│   ├── config.py          # Configuration
│   ├── database.py        # Database connection
│   └── security.py        # Security utilities
│
├── schemas/                # Pydantic schemas
│   ├── __init__.py
│   ├── chat.py
│   └── system.py
│
├── main.py                 # FastAPI application entry
├── requirements.txt
└── .env.example
```

### Voice Service (`/voice-service`)

```
voice-service/
├── recognition/            # Speech-to-text
│   ├── __init__.py
│   └── recognizer.py
│
├── synthesis/              # Text-to-speech
│   ├── __init__.py
│   └── synthesizer.py
│
├── wake_word/              # Wake word detection
│   ├── __init__.py
│   └── detector.py
│
├── voice_service.py        # Main service
├── requirements.txt
└── config.py
```

## Communication Flow

### Chat Message Flow

```
1. User types message in Frontend
   ↓
2. Frontend sends via WebSocket to Backend
   ↓
3. Backend processes message with AI Service (Groq)
   ↓
4. Backend saves to Database (SQLite)
   ↓
5. Backend sends response via WebSocket to Frontend
   ↓
6. Frontend displays response in Chat UI
```

### Voice Command Flow

```
1. Voice Service detects wake word
   ↓
2. Voice Service records audio
   ↓
3. Voice Service converts speech to text
   ↓
4. Text sent to Backend via REST API
   ↓
5. Backend processes with AI Service
   ↓
6. Backend sends response to Frontend
   ↓
7. Frontend sends to Voice Service for TTS
   ↓
8. Voice Service speaks response
```

## Database Schema

### Conversations Table
```sql
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Messages Table
```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER NOT NULL,
    role TEXT NOT NULL,  -- 'user' or 'assistant'
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);
```

### Settings Table
```sql
CREATE TABLE settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## API Endpoints

### Chat Endpoints
- `POST /api/chat/message` - Send a chat message
- `GET /api/chat/conversations` - Get all conversations
- `GET /api/chat/conversations/{id}` - Get specific conversation
- `DELETE /api/chat/conversations/{id}` - Delete conversation

### System Endpoints
- `POST /api/system/execute` - Execute system command
- `GET /api/system/status` - Get system status
- `POST /api/system/app/open` - Open application
- `POST /api/system/app/close` - Close application

### WebSocket
- `WS /ws` - WebSocket connection for real-time chat

## Security Considerations

1. **API Keys**: Stored in environment variables, never in code
2. **Data Privacy**: All data stored locally by default
3. **System Access**: Permission-based execution of system commands
4. **WebSocket**: Secure WebSocket (WSS) for production
5. **Input Validation**: All inputs validated using Pydantic

## Performance Targets

- **Response Time**: < 500ms for chat messages
- **Memory Usage**: < 150MB idle
- **CPU Usage**: < 5% idle
- **Startup Time**: < 2 seconds
- **Voice Recognition Accuracy**: > 95%

## Future Extensions

1. **Plugin System**: Allow third-party plugins
2. **Cloud Sync**: Optional cloud synchronization
3. **Mobile App**: Companion mobile application
4. **Multi-language**: Full internationalization
5. **Custom AI Models**: Support for local models