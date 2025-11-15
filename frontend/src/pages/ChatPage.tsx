import { useEffect, useState } from 'react';
import ChatMessage from '../components/Chat/ChatMessage';
import ChatInput from '../components/Chat/ChatInput';
import Header from '../components/Layout/Header';
import { useChatStore } from '../store/chatStore';
import { wsService } from '../services/websocket';
import { Loader2 } from 'lucide-react';

function ChatPage() {
  const { messages, addMessage, isLoading } = useChatStore();
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // Connect to WebSocket
    wsService
      .connect()
      .then(() => {
        setIsConnected(true);
      })
      .catch((error) => {
        console.error('Failed to connect to WebSocket:', error);
        setIsConnected(false);
      });

    // Listen for messages
    wsService.onMessage((data) => {
      addMessage({
        role: 'assistant',
        content: data.message || data,
      });
    });

    return () => {
      wsService.disconnect();
    };
  }, [addMessage]);

  const handleSendMessage = (content: string) => {
    // Add user message
    addMessage({
      role: 'user',
      content,
    });

    // Send to backend
    if (wsService.isConnected()) {
      wsService.send({ message: content });
    } else {
      console.error('WebSocket not connected');
      addMessage({
        role: 'assistant',
        content: '❌ Connection error. Please check if the backend is running.',
      });
    }
  };

  return (
    <div className="flex flex-col h-full">
      <Header isConnected={isConnected} />
      
      <div className="flex-1 overflow-hidden flex flex-col">
        {/* Messages Container */}
        <div className="flex-1 overflow-y-auto px-4 py-6 scrollbar-thin">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center">
              <div className="glass-heavy rounded-2xl p-8 max-w-md">
                <h2 className="text-2xl font-bold text-gray-800 dark:text-white mb-4">
                  👋 Welcome to Windows AI Assistant
                </h2>
                <p className="text-gray-600 dark:text-gray-400">
                  Start a conversation by typing a message below or click the microphone to use voice input.
                </p>
              </div>
            </div>
          ) : (
            <div className="max-w-4xl mx-auto space-y-4">
              {messages.map((message) => (
                <ChatMessage key={message.id} message={message} />
              ))}
              {isLoading && (
                <div className="flex items-center gap-2 text-gray-500 dark:text-gray-400">
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>AI is thinking...</span>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Input Container */}
        <div className="border-t border-gray-200 dark:border-dark-700 bg-white/50 dark:bg-dark-800/50 backdrop-blur-xl">
          <div className="max-w-4xl mx-auto px-4 py-4">
            <ChatInput onSend={handleSendMessage} disabled={!isConnected} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default ChatPage;