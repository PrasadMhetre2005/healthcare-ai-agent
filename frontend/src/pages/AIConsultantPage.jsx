import React, { useState, useRef, useEffect } from 'react';
import { Send, ArrowLeft, Mic, Activity, CheckCircle, Calendar, Search, X } from 'lucide-react';
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
  const [searchQuery, setSearchQuery] = useState('');
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

  // Filter messages based on search query
  const filteredMessages = messages.filter(msg =>
    msg.text.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const displayMessages = searchQuery ? filteredMessages : messages;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-cyan-50 flex flex-col">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 via-blue-700 to-blue-800 text-white p-6 shadow-xl border-b-4 border-blue-900">
        <div className="max-w-6xl mx-auto">
          <div className="flex items-center gap-4 mb-4">
            <button
              onClick={() => navigate('/dashboard')}
              className="hover:bg-blue-500/30 p-2 rounded-lg transition-colors duration-200 hover:scale-110 transform"
              title="Back to Dashboard"
            >
              <ArrowLeft className="w-6 h-6" />
            </button>
            <div className="flex-1">
              <h1 className="text-4xl font-bold tracking-tight">Healthcare AI Consultant</h1>
              <p className="text-blue-100 mt-1 text-lg">Your Personal Health & Wellness Assistant</p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 max-w-6xl w-full mx-auto p-6 flex flex-col">
        {/* Messages Container */}
        <div className="flex-1 bg-white rounded-2xl shadow-lg p-8 mb-6 overflow-y-auto space-y-4 border border-gray-100">
          {messages.length === 1 ? (
            <div className="flex flex-col items-center justify-center h-full py-12">
              {/* Welcome Avatar and Message */}
              <div className="text-center space-y-8">
                <div className="flex justify-center">
                  <div className="w-32 h-32 bg-gradient-to-br from-blue-400 via-blue-500 to-cyan-600 rounded-full flex items-center justify-center text-7xl shadow-2xl transform hover:scale-110 transition-transform duration-300">
                    🤖
                  </div>
                </div>
                <div>
                  <h2 className="text-4xl font-bold text-gray-900 mb-2 tracking-tight">
                    {messages[0].text}
                  </h2>
                  <p className="text-xl text-gray-600">Ask or describe symptoms</p>
                </div>
              </div>

              {/* Quick Actions */}
              <div className="w-full space-y-3 mt-12 max-w-md">
                <button
                  onClick={() => handleQuickAction('symptoms')}
                  className="w-full flex items-center gap-3 px-6 py-4 bg-gradient-to-r from-green-50 to-green-100 hover:from-green-100 hover:to-green-200 text-green-700 rounded-xl transition-all duration-200 font-semibold text-lg shadow-md hover:shadow-lg hover:scale-105 transform border border-green-200"
                >
                  <CheckCircle className="w-6 h-6 flex-shrink-0" />
                  <span>Start Symptom Check</span>
                </button>
                <button
                  onClick={() => handleQuickAction('vitals')}
                  className="w-full flex items-center gap-3 px-6 py-4 bg-gradient-to-r from-blue-50 to-blue-100 hover:from-blue-100 hover:to-blue-200 text-blue-700 rounded-xl transition-all duration-200 font-semibold text-lg shadow-md hover:shadow-lg hover:scale-105 transform border border-blue-200"
                >
                  <Activity className="w-6 h-6 flex-shrink-0" />
                  <span>View Your Vitals</span>
                </button>
                <button
                  onClick={() => handleQuickAction('appointment')}
                  className="w-full flex items-center gap-3 px-6 py-4 bg-gradient-to-r from-orange-50 to-orange-100 hover:from-orange-100 hover:to-orange-200 text-orange-700 rounded-xl transition-all duration-200 font-semibold text-lg shadow-md hover:shadow-lg hover:scale-105 transform border border-orange-200"
                >
                  <Calendar className="w-6 h-6 flex-shrink-0" />
                  <span>Check Appointments</span>
                </button>
              </div>
            </div>
          ) : (
            <>
              {/* Search Bar */}
              <div className="sticky top-0 bg-white rounded-lg p-4 mb-4 border border-gray-200 shadow-sm">
                <div className="flex items-center gap-3">
                  <Search className="w-5 h-5 text-gray-400" />
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Search messages..."
                    className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                  />
                  {searchQuery && (
                    <button
                      onClick={() => setSearchQuery('')}
                      className="p-1 hover:bg-gray-100 rounded-lg transition-colors"
                    >
                      <X className="w-5 h-5 text-gray-400" />
                    </button>
                  )}
                </div>
                {searchQuery && (
                  <p className="text-sm text-gray-500 mt-2">Found {filteredMessages.length} of {messages.length} messages</p>
                )}
              </div>

              {/* Messages List */}
              {displayMessages.length > 1 ? (
                displayMessages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'} animate-fadeIn`}
                  >
                    <div
                      className={`max-w-2xl px-6 py-4 rounded-2xl ${
                        message.sender === 'user'
                          ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-br-none shadow-md'
                          : 'bg-gray-100 text-gray-900 rounded-bl-none shadow-sm'
                      }`}
                    >
                      <p className="text-base whitespace-pre-wrap leading-relaxed">{message.text}</p>
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
                ))
              ) : (
                <div className="text-center py-8 text-gray-500">
                  <p>No messages match your search.</p>
                </div>
              )}
              
              {loading && (
                <div className="flex justify-start animate-fadeIn">
                  <div className="bg-gray-100 text-gray-900 px-6 py-4 rounded-2xl rounded-bl-none shadow-sm">
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
        {messages.length > 1 && !searchQuery && (
          <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
            <div className="flex gap-3">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask me anything about your health..."
                className="flex-1 px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-transparent text-base placeholder-gray-500 transition-all"
                disabled={loading}
              />
              <button
                className="hover:bg-gray-100 p-3 rounded-xl transition-colors text-gray-600 hover:text-gray-900 transform hover:scale-110"
                title="Voice input"
              >
                <Mic className="w-6 h-6" />
              </button>
              <button
                onClick={() => handleSendMessage()}
                disabled={loading || !inputValue.trim()}
                className="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 disabled:from-gray-400 disabled:to-gray-500 text-white px-6 py-3 rounded-xl transition-all duration-200 flex items-center gap-2 font-semibold shadow-md hover:shadow-lg transform hover:scale-105 disabled:scale-100"
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
