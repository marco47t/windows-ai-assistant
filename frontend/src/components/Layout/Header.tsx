import { Moon, Sun, Settings, Circle } from 'lucide-react';
import { useThemeStore } from '../../store/themeStore';

interface HeaderProps {
  isConnected: boolean;
}

function Header({ isConnected }: HeaderProps) {
  const { theme, toggleTheme } = useThemeStore();

  return (
    <header className="glass border-b border-gray-200/20 dark:border-dark-700/20">
      <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl flex items-center justify-center">
            <span className="text-white font-bold text-lg">AI</span>
          </div>
          <div>
            <h1 className="text-xl font-bold text-gray-800 dark:text-white">
              Windows AI Assistant
            </h1>
            <div className="flex items-center gap-2">
              <Circle
                className={`w-2 h-2 fill-current ${
                  isConnected ? 'text-green-500' : 'text-red-500'
                }`}
              />
              <span className="text-xs text-gray-500 dark:text-gray-400">
                {isConnected ? 'Connected' : 'Disconnected'}
              </span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={toggleTheme}
            className="p-2 rounded-lg hover:bg-gray-200/50 dark:hover:bg-dark-700/50 transition-colors"
            aria-label="Toggle theme"
          >
            {theme === 'light' ? (
              <Moon className="w-5 h-5 text-gray-700 dark:text-gray-300" />
            ) : (
              <Sun className="w-5 h-5 text-gray-700 dark:text-gray-300" />
            )}
          </button>
          <button
            className="p-2 rounded-lg hover:bg-gray-200/50 dark:hover:bg-dark-700/50 transition-colors"
            aria-label="Settings"
          >
            <Settings className="w-5 h-5 text-gray-700 dark:text-gray-300" />
          </button>
        </div>
      </div>
    </header>
  );
}

export default Header;