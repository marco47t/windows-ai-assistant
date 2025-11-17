# 🤖 Windows AI Assistant

> Intelligent AI assistant with Groq and Gemini integration, smart provider routing, and CLI interface.

![Python](https://img.shields.io/badge/python-3.11+-blue)
![Groq](https://img.shields.io/badge/AI-Groq-orange)
![Gemini](https://img.shields.io/badge/AI-Gemini-4285F4)

## ✨ Features

- 🚀 **Dual AI Providers**: Groq (fast) + Gemini (powerful)
- 🧠 **Intelligent Routing**: Automatically picks the best AI based on task
- 💬 **CLI Interface**: Simple command-line chat
- 💾 **Chat History**: SQLite database for conversations
- ⚡ **Fast Responses**: Optimized for speed
- 🔄 **Easy Switching**: Manual provider override available

## 🎯 AI Provider Selection

**Groq** is used for:
- Quick chat responses
- Short queries (< 1000 tokens)
- Real-time conversations

**Gemini** is used for:
- Long documents analysis
- Complex reasoning tasks
- Large context (> 1000 tokens)

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Groq API key (free at [console.groq.com](https://console.groq.com))
- Gemini API key (optional, free at [ai.google.dev](https://ai.google.dev))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/marco47t/windows-ai-assistant.git
cd windows-ai-assistant
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

5. **Run the CLI**
```bash
python cli.py
```

## 📁 Project Structure

```
windows-ai-assistant/
├── cli.py                 # CLI interface
├── core/
│   ├── config.py         # Configuration
│   ├── database.py       # Database setup
│   └── logger.py         # Logging
├── services/
│   ├── ai_provider.py    # AI provider interface
│   ├── groq_service.py   # Groq integration
│   ├── gemini_service.py # Gemini integration
│   ├── router.py         # Smart routing logic
│   └── chat_service.py   # Chat management
├── models/
│   └── chat.py           # Database models
├── .env.example          # Environment template
└── requirements.txt      # Dependencies
```

## 🎮 Usage

### CLI Mode
```bash
python cli.py
```

**Commands:**
- Type your message to chat
- `!groq` - Force use Groq
- `!gemini` - Force use Gemini
- `!auto` - Auto-select provider (default)
- `!history` - View chat history
- `!clear` - Clear conversation
- `!exit` or `!quit` - Exit

### Examples

```bash
# Normal chat (auto-selects provider)
You: What is machine learning?
AI: [Groq] Machine learning is...

# Force Gemini for complex task
You: !gemini
You: Analyze this 5000-word document...
AI: [Gemini] Based on my analysis...

# Switch back to auto
You: !auto
```

## ⚙️ Configuration

Edit `.env` file:

```env
# AI Provider Keys
GROQ_API_KEY=your_groq_key_here
GEMINI_API_KEY=your_gemini_key_here  # Optional

# Default Provider (groq, gemini, or auto)
DEFAULT_PROVIDER=auto

# Token threshold for auto-routing
ROUTING_TOKEN_THRESHOLD=1000

# Database
DATABASE_URL=sqlite:///data/assistant.db
```

## 🔧 Development

### Run Tests
```bash
python -m pytest tests/
```

### Add New Provider
1. Create new service in `services/`
2. Implement `AIProvider` interface
3. Update `router.py` logic

## 📊 Rate Limits

### Groq (Free)
- 30 requests/min
- 14,400 requests/day
- 6,000 tokens/min
- 500,000 tokens/day

### Gemini 2.5 Flash (Free)
- 10 requests/min
- 250 requests/day
- 250,000 tokens/min

## 🗺️ Roadmap

- [x] CLI interface
- [x] Groq integration
- [x] Gemini integration
- [x] Smart routing
- [x] Chat history
- [ ] FastAPI server
- [ ] Voice commands
- [ ] System control
- [ ] Frontend UI

## 📝 License

MIT License

## 🙏 Acknowledgments

- [Groq](https://groq.com) for fast AI inference
- [Google Gemini](https://ai.google.dev) for powerful AI models

---

**Built with ❤️ by [marco47t](https://github.com/marco47t)**