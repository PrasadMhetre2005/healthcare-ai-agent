import React, { useState, useRef, useEffect } from 'react';
import { Send, ArrowLeft, Mic, Activity, CheckCircle, Calendar } from 'lucide-react';
import { useNavigate, useLocation } from 'react-router-dom';
import { chatService } from '../services/api';
import { useAuth } from '../hooks/useAuth';
import toast from 'react-hot-toast';

export const AIConsultantPage = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [isInitialized, setIsInitialized] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const initializeChat = () => {
    setMessages([
      {
        id: 1,
        text: `Hi ${user?.username || 'there'}, how can I help you?`,
        sender: 'bot',
        timestamp: new Date(),
      }
    ]);
    setIsInitialized(true);
  };

  useEffect(() => {
    initializeChat();
  }, []);

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

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-white flex flex-col">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-6 shadow-lg">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate('/dashboard')}
              className="hover:bg-blue-500 p-2 rounded-lg transition-colors"
              title="Back to Dashboard"
            >
              <ArrowLeft className="w-6 h-6" />
            </button>
            <div>
              <h1 className="text-3xl font-bold">Healthcare AI Consultant</h1>
              <p className="text-blue-100 mt-1">Your Personal Health Assistant</p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 max-w-4xl w-full mx-auto p-6 flex flex-col">
        {/* Messages Container */}
        <div className="flex-1 bg-white rounded-lg shadow-md p-6 mb-4 overflow-y-auto space-y-4 border border-gray-200">
          {messages.length === 1 ? (
            <div className="flex flex-col items-center justify-center h-full py-12">
              {/* Welcome Avatar and Message */}
              <div className="text-center space-y-8">
                <div className="flex justify-center">
                  <div className="w-32 h-32 bg-gradient-to-br from-blue-400 to-blue-600 rounded-full flex items-center justify-center text-7xl shadow-lg">
                    🤖
                  </div>
                </div>
                <div>
                  <h2 className="text-3xl font-bold text-gray-900 mb-2">
                    {messages[0].text}
                  </h2>
                  <p className="text-lg text-gray-600">Ask or describe symptoms</p>
                </div>
              </div>

              {/* Quick Actions */}
              <div className="w-full space-y-4 mt-12 max-w-md">
                <button
                  onClick={() => handleQuickAction('symptoms')}
                  className="w-full flex items-center gap-3 px-6 py-4 bg-green-100 hover:bg-green-200 text-green-700 rounded-lg transition-colors font-semibold text-lg"
                >
                  <CheckCircle className="w-6 h-6" />
                  <span>Start Symptom Check</span>
                </button>
                <button
                  onClick={() => handleQuickAction('vitals')}
                  className="w-full flex items-center gap-3 px-6 py-4 bg-blue-100 hover:bg-blue-200 text-blue-700 rounded-lg transition-colors font-semibold text-lg"
                >
                  <Activity className="w-6 h-6" />
                  <span>View Your Vitals</span>
                </button>
                <button
                  onClick={() => handleQuickAction('appointment')}
                  className="w-full flex items-center gap-3 px-6 py-4 bg-orange-100 hover:bg-orange-200 text-orange-700 rounded-lg transition-colors font-semibold text-lg"
                >
                  <Calendar className="w-6 h-6" />
                  <span>Check Appointments</span>
                </button>
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
                    className={`max-w-2xl px-6 py-3 rounded-lg ${
                      message.sender === 'user'
                        ? 'bg-blue-600 text-white rounded-br-none'
                        : 'bg-gray-200 text-gray-900 rounded-bl-none'
                    }`}
                  >
                    <p className="text-base whitespace-pre-wrap">{message.text}</p>
                    <p
                      className={`text-sm mt-2 ${
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
                  <div className="bg-gray-200 text-gray-900 px-6 py-3 rounded-lg rounded-bl-none">
                    <div className="flex gap-2">
                      <div className="w-3 h-3 bg-gray-600 rounded-full animate-bounce" />
                      <div className="w-3 h-3 bg-gray-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                      <div className="w-3 h-3 bg-gray-600 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }} />
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
          <div className="bg-white rounded-lg shadow-md p-4 border border-gray-200">
            <div className="flex gap-3">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type or speak a question..."
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600 text-base"
                disabled={loading}
              />
              <button
                className="hover:bg-gray-100 p-3 rounded-lg transition-colors text-gray-600"
                title="Voice input"
              >
                <Mic className="w-6 h-6" />
              </button>
              <button
                onClick={() => handleSendMessage()}
                disabled={loading || !inputValue.trim()}
                className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-6 py-3 rounded-lg transition-colors flex items-center gap-2 font-semibold"
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
