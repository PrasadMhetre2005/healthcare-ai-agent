import React, { useState, useRef, useEffect } from 'react';
import { Send, MessageCircle, X, Minimize2, Maximize2, Mic, Activity, CheckCircle, Calendar } from 'lucide-react';
import { chatService } from '../services/api';
import { useAuth } from '../hooks/useAuth';
import toast from 'react-hot-toast';

export const AIHealthcareChat = () => {
  const { user } = useAuth();
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const initializeChat = () => {
    setIsOpen(true);
    setMessages([
      {
        id: 1,
        text: `Hi ${user?.username || 'there'}, how can I help you?`,
        sender: 'bot',
        timestamp: new Date(),
      }
    ]);
  };

  const handleQuickAction = (action) => {
    let message = '';
    switch(action) {
      case 'symptoms':
        message = 'I want to check my symptoms';
        break;
      case 'vitals':
        message = 'Show me my latest vital signs';
        break;
      case 'appointment':
        message = 'When is my next appointment?';
        break;
      default:
        message = action;
    }
    
    setInputValue(message);
    handleSendMessage(message);
  };

  const handleSendMessage = async (messageText = null) => {
    const text = messageText || inputValue;
    if (!text.trim()) return;

    const userMessage = {
      id: messages.length + 1,
      text: text,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setLoading(true);

    try {
      const response = await chatService.sendMessage(text);

      const botMessage = {
        id: messages.length + 2,
        text: response.response,
        sender: 'bot',
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage = {
        id: messages.length + 2,
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'bot',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
      toast.error('Failed to get response from AI consultant');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Welcome Screen - Show before messages
  if (!isOpen) {
    return (
      <div className="fixed bottom-4 right-4 z-40">
        <button
          onClick={initializeChat}
          className="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white rounded-full p-4 shadow-lg transition-all transform hover:scale-110"
          title="Open Healthcare Chat"
        >
          <MessageCircle className="w-6 h-6" />
        </button>
      </div>
    );
  }

  if (isMinimized) {
    return (
      <div className="fixed bottom-4 right-4 z-40">
        <button
          onClick={() => setIsMinimized(false)}
          className="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white rounded-full p-4 shadow-lg transition-all transform hover:scale-110"
          title="Open Healthcare Chat"
        >
          <MessageCircle className="w-6 h-6" />
        </button>
      </div>
    );
  }

  const chatClass = isExpanded
    ? 'fixed bottom-0 right-0 w-full h-full z-50'
    : 'fixed bottom-4 right-4 w-96 h-[500px] z-40 rounded-lg shadow-2xl';

  return (
    <div className={`bg-white flex flex-col ${chatClass} overflow-hidden`}>
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-4 rounded-t-lg flex items-center justify-between">
        <div className="flex items-center gap-3">
          <MessageCircle className="w-5 h-5" />
          <div>
            <h3 className="font-semibold">Healthcare AI</h3>
            <p className="text-xs text-blue-100">Always here to help</p>
          </div>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="hover:bg-blue-500 p-2 rounded transition-colors"
            title={isExpanded ? 'Minimize' : 'Expand'}
          >
            {isExpanded ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
          </button>
          <button
            onClick={() => {
              setIsMinimized(true);
              setIsOpen(false);
              setMessages([]);
            }}
            className="hover:bg-blue-500 p-2 rounded transition-colors"
            title="Close"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-6 bg-gradient-to-b from-blue-50 to-white space-y-4">
        {messages.length === 1 ? (
          <div className="flex flex-col items-center justify-start h-full">
            {/* Welcome Avatar and Message */}
            <div className="text-center space-y-6 mb-8">
              <div className="flex justify-center">
                <div className="w-24 h-24 bg-gradient-to-br from-blue-400 to-blue-600 rounded-full flex items-center justify-center text-5xl shadow-lg">
                  🤖
                </div>
              </div>
              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-2">
                  {messages[0].text}
                </h2>
                <p className="text-gray-600">Ask or describe symptoms</p>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="w-full space-y-3">
              <div className="flex gap-3 flex-wrap justify-center">
                <button
                  onClick={() => handleQuickAction('symptoms')}
                  className="flex items-center gap-2 px-4 py-3 bg-green-100 hover:bg-green-200 text-green-700 rounded-lg transition-colors font-medium"
                >
                  <CheckCircle className="w-5 h-5" />
                  <span>Start Symptom Check</span>
                </button>
              </div>
              <div className="flex gap-3 flex-wrap justify-center">
                <button
                  onClick={() => handleQuickAction('vitals')}
                  className="flex items-center gap-2 px-4 py-3 bg-blue-100 hover:bg-blue-200 text-blue-700 rounded-lg transition-colors font-medium"
                >
                  <Activity className="w-5 h-5" />
                  <span>View Your Vitals</span>
                </button>
              </div>
              <div className="flex gap-3 flex-wrap justify-center">
                <button
                  onClick={() => handleQuickAction('appointment')}
                  className="flex items-center gap-2 px-4 py-3 bg-orange-100 hover:bg-orange-200 text-orange-700 rounded-lg transition-colors font-medium"
                >
                  <Calendar className="w-5 h-5" />
                  <span>Check Appointments</span>
                </button>
              </div>
            </div>
          </div>
        ) : (
          <>
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-xs lg:max-w-md px-4 py-3 rounded-lg ${
                    message.sender === 'user'
                      ? 'bg-blue-600 text-white rounded-br-none'
                      : 'bg-gray-200 text-gray-900 rounded-bl-none'
                  }`}
                >
                  <p className="text-sm whitespace-pre-wrap">{message.text}</p>
                  <p
                    className={`text-xs mt-2 ${
                      message.sender === 'user' ? 'text-blue-100' : 'text-gray-600'
                    }`}
                  >
                    {message.timestamp.toLocaleTimeString([], {
                      hour: '2-digit',
                      minute: '2-digit',
                    })}
                  </p>
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex justify-start">
                <div className="bg-gray-200 text-gray-900 px-4 py-2 rounded-lg rounded-bl-none">
                  <div className="flex gap-2">
                    <div className="w-2 h-2 bg-gray-600 rounded-full animate-bounce" />
                    <div className="w-2 h-2 bg-gray-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                    <div className="w-2 h-2 bg-gray-600 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }} />
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Input Container */}
      {messages.length > 1 && (
        <div className="border-t bg-white p-4 rounded-b-lg">
          <div className="flex gap-2">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type or speak a question..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600 text-sm"
              disabled={loading}
            />
            <button
              className="hover:bg-gray-100 p-2 rounded-lg transition-colors text-gray-600"
              title="Voice input"
            >
              <Mic className="w-5 h-5" />
            </button>
            <button
              onClick={() => handleSendMessage()}
              disabled={loading || !inputValue.trim()}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-4 py-2 rounded-lg transition-colors flex items-center gap-2"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
