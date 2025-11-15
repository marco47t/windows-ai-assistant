import { useState } from 'react';
import ChatPage from './pages/ChatPage';
import { useThemeStore } from './store/themeStore';

function App() {
  const { theme } = useThemeStore();

  return (
    <div className={`${theme === 'dark' ? 'dark' : ''} h-screen`}>
      <div className="h-full bg-gradient-to-br from-gray-50 to-gray-100 dark:from-dark-900 dark:to-dark-800">
        <ChatPage />
      </div>
    </div>
  );
}

export default App;