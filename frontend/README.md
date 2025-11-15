# Frontend - Windows AI Assistant

Modern React + TypeScript + Electron frontend with glassmorphic design.

## 🛠️ Tech Stack

- **React 19** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool & dev server
- **Electron** - Desktop application wrapper
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations
- **Zustand** - State management
- **Lucide React** - Icon library

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

The app will open at `http://localhost:5173`

### Run as Electron App

1. Start dev server and Electron together:
```bash
npm run electron:dev
```

This will:
- Start Vite dev server on port 5173
- Wait for server to be ready
- Launch Electron window
- Enable hot reload

## 📚 Project Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── Chat/            # Chat-related components
│   │   │   ├── ChatMessage.tsx
│   │   │   └── ChatInput.tsx
│   │   └── Layout/          # Layout components
│   │       └── Header.tsx
│   │
│   ├── pages/              # Page components
│   │   └── ChatPage.tsx
│   │
│   ├── services/           # API services
│   │   ├── api.ts           # REST API
│   │   └── websocket.ts     # WebSocket client
│   │
│   ├── store/              # Zustand stores
│   │   ├── chatStore.ts
│   │   └── themeStore.ts
│   │
│   ├── types/              # TypeScript types
│   │   └── chat.ts
│   │
│   ├── styles/             # Global styles
│   │   └── globals.css
│   │
│   ├── App.tsx             # Root component
│   └── main.tsx            # Entry point
│
├── electron/              # Electron main process
│   ├── main.js
│   └── preload.js
│
├── public/                # Static assets
├── index.html             # HTML entry
├── vite.config.ts         # Vite configuration
├── tailwind.config.js     # Tailwind configuration
├── tsconfig.json          # TypeScript config
└── package.json           # Dependencies
```

## ⚙️ Available Scripts

### Development
```bash
npm run dev              # Start Vite dev server
npm run electron         # Start Electron (requires dev server)
npm run electron:dev     # Start both dev server + Electron
```

### Building
```bash
npm run build           # Build for production
npm run preview         # Preview production build
npm run electron:build  # Build Electron app
```

### Code Quality
```bash
npm run lint            # Run ESLint
npm run format          # Format with Prettier
```

## 🎨 Features

### Glassmorphic Design
The UI uses a modern glassmorphic design with:
- Frosted glass effect backgrounds
- Subtle borders and shadows
- Smooth animations
- Dark/Light theme support

### Chat Interface
- Real-time messaging
- WebSocket connection
- Auto-scroll to latest message
- Typing indicators
- Message timestamps

### Voice Input (Coming Soon)
- Microphone button in chat input
- Real-time speech recognition
- Visual recording indicator

### Theme Switching
- Dark mode (default)
- Light mode
- System theme detection
- Persistent preference

## 🔌 WebSocket Connection

The frontend connects to the backend WebSocket server at:
```
ws://localhost:8000/ws
```

**Connection Status:**
- Green dot = Connected
- Red dot = Disconnected

The WebSocket service includes:
- Auto-reconnect (5 attempts)
- Connection state management
- Error handling

## 📦 Building for Production

### Web Build
```bash
npm run build
```

Output: `build/` directory

### Electron Build
```bash
npm run electron:build
```

This will create:
- Windows: `.exe` installer in `dist/`
- Portable version
- Auto-updater ready

## 🔧 Configuration

### API Endpoints

Edit `src/services/api.ts` to change backend URL:
```typescript
const API_BASE_URL = 'http://localhost:8000';
```

### WebSocket URL

Edit `src/services/websocket.ts`:
```typescript
const wsUrl = 'ws://localhost:8000/ws';
```

### Electron Window

Edit `electron/main.js` to customize:
- Window size
- Frame style
- System tray behavior

## 🎨 Customizing Theme

Edit `tailwind.config.js` to customize colors:

```javascript
theme: {
  extend: {
    colors: {
      primary: { /* your colors */ },
      dark: { /* your colors */ },
    },
  },
}
```

## 🐛 Troubleshooting

### Port Already in Use
If port 5173 is busy:
```bash
# Change port in vite.config.ts
server: {
  port: 3000,
}
```

### WebSocket Connection Failed
1. Ensure backend is running on port 8000
2. Check backend logs for errors
3. Verify CORS settings in backend

### Electron Not Starting
```bash
# Install Electron explicitly
npm install electron --save-dev

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### TypeScript Errors
```bash
# Check TypeScript version
npm list typescript

# Reinstall types
npm install --save-dev @types/react @types/react-dom
```

## 📡 Next Steps

1. **Backend Integration**
   - Start backend server
   - Test WebSocket connection
   - Implement AI responses

2. **Voice Features**
   - Add microphone permissions
   - Integrate with voice service
   - Add voice feedback

3. **UI Enhancements**
   - Add settings page
   - Implement conversation history
   - Add system tray menu

4. **System Integration**
   - File system operations
   - Application control
   - System notifications

## 📝 Notes

- Backend must be running for full functionality
- Voice features require backend voice service
- System tray works only in Electron build
- Hot reload enabled in development mode

---

**Ready to start?** Run `npm install && npm run electron:dev` to get started! 🚀