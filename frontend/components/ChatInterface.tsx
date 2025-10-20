'use client';

import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send } from 'lucide-react';
import PropertyCard from './PropertyCard';

interface Message {
  id: number;
  type: 'user' | 'bot';
  content: string;
  properties?: Property[];
  timestamp: Date;
}

interface Property {
  title: string;
  type: string;
  price: string;
  carpet_area: string;
  location: string;
  full_address: string;
  status: string;
  bathrooms: number | string;
  balcony: number;
  furnished: string;
  possession: string;
  slug: string;
  image?: string;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      type: 'bot',
      content: "Hi! I'm your property search assistant. Tell me what you're looking for. For example: '3BHK flat in Pune under ₹1.2 Cr' or 'Ready to move 2BHK in Mumbai'",
      timestamp: new Date(),
    },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage: Message = {
      id: messages.length + 1,
      type: 'user',
      content: inputValue,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_URL}/chat`, {
        message: inputValue,
      });

      const botMessage: Message = {
        id: messages.length + 2,
        type: 'bot',
        content: response.data.summary,
        properties: response.data.properties,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: messages.length + 2,
        type: 'bot',
        content: 'Sorry, I encountered an error. Please make sure the backend is running on http://localhost:5000',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="max-w-6xl mx-auto bg-white rounded-2xl shadow-2xl overflow-hidden flex flex-col h-[80vh]">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-gray-50">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-3xl ${
                message.type === 'user'
                  ? 'bg-blue-600 text-white rounded-2xl rounded-br-none'
                  : 'bg-white text-gray-800 rounded-2xl rounded-bl-none border border-gray-200'
              } px-6 py-4 shadow-md`}
            >
              <p className="text-sm leading-relaxed">{message.content}</p>
              
              {/* Property Cards */}
              {message.properties && message.properties.length > 0 && (
                <div className="mt-4 space-y-3">
                  <p className="text-xs font-semibold text-gray-700 mb-2">
                    {message.properties.length} {message.properties.length === 1 ? 'Property' : 'Properties'} Found:
                  </p>
                  <div className="grid grid-cols-1 gap-3">
                    {message.properties.map((property, idx) => (
                      <PropertyCard key={idx} property={property} />
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white rounded-2xl rounded-bl-none px-6 py-4 border border-gray-200 shadow-md">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area - FIXED FOR BETTER VISIBILITY */}
      <div className="border-t border-gray-200 p-4 bg-white">
        <div className="flex space-x-4">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your query... e.g., '3BHK in Pune under 1.5 Cr'"
            className="flex-1 px-4 py-3 border-2 border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white text-gray-900 placeholder:text-gray-500 font-medium"
            disabled={isLoading}
          />
          <button
            onClick={handleSendMessage}
            disabled={isLoading || !inputValue.trim()}
            className="bg-blue-600 text-white px-6 py-3 rounded-xl hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center space-x-2 font-medium"
          >
            <Send size={20} />
            <span>Send</span>
          </button>
        </div>
        
        {/* Example Queries - FIXED FOR BETTER VISIBILITY */}
        <div className="mt-3 flex flex-wrap gap-2 items-center">
          <span className="text-sm text-gray-700 font-semibold">Try:</span>
          {['3BHK in Pune under 1.2 Cr', 'Ready to move 2BHK', 'Office space in Mumbai'].map((example) => (
            <button
              key={example}
              onClick={() => setInputValue(example)}
              className="text-sm bg-blue-50 text-blue-700 border border-blue-300 px-4 py-1.5 rounded-full hover:bg-blue-100 hover:border-blue-400 transition-colors font-medium shadow-sm"
            >
              {example}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

