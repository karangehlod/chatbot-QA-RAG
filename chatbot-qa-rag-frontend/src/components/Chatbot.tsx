import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios'; // Import axios directly
import { v4 as uuidv4 } from 'uuid';
import ChatHeader from './ChatHeader';
import ChatMessages from './ChatMessages';
import ChatInput from './ChatInput';
import '../styles/ChatPage.css';

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'ai';
  timestamp: string;
  type?: 'text' | 'code' | 'error';
}

const ChatPage: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();

  // Initial welcome message
  useEffect(() => {
    const welcomeMessage: Message = {
      id: uuidv4(),
      content: "Hello! I'm your AI assistant. How can I help you today?",
      sender: 'ai',
      timestamp: new Date().toISOString(),
      type: 'text'
    };
    setMessages([welcomeMessage]);
  }, []);

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (message: string) => {
    // Add user message
    const userMessage: Message = {
      id: uuidv4(),
      content: message,
      sender: 'user',
      timestamp: new Date().toISOString(),
      type: 'text'
    };

    setMessages(prevMessages => [...prevMessages, userMessage]);
    setIsLoading(true);

    try {
      // Detailed logging for debugging
      console.log('Sending message:', message);

      // Use axios directly with full configuration
      const response = await axios.post('http://localhost:8000/api/query/', 
        { query: message },
        {
          headers: {
            'Content-Type': 'application/json',
            // Add any authentication headers if needed
            // 'Authorization': `Bearer ${your_token}`
          },
          timeout: 100000 // 100 seconds timeout
        }
      );

      // Log the full response for debugging
      console.log('Full API Response:', response);
      
      // Flexible response handling
      const aiMessageContent = response.data.message || 
        response.data.response || 
        "I received a response, but it's not in the expected format.";

      const aiMessage: Message = {
        id: uuidv4(),
        content: aiMessageContent,
        sender: 'ai',
        timestamp: new Date().toISOString(),
        type: response.data.type || 'text'
      };

      setMessages(prevMessages => [...prevMessages, aiMessage]);
    } catch (error) {
      // Comprehensive error logging
      if (axios.isAxiosError(error)) {
        console.error('Axios Error:', {
          message: error.message,
          status: error.response?.status,
          data: error.response?.data
        });
      } else {
        console.error('Unexpected Error:', error);
      }

      const errorMessage: Message = {
        id: uuidv4(),
        content: (() => {
          if (axios.isAxiosError(error)) {
            if (error.response) {
              // The request was made and the server responded with a status code
              return error.response.data.message || 
                     `Server Error: ${error.response.status}`;
            } else if (error.request) {
              // The request was made but no response was received
              return "No response received from the server. Please check your connection.";
            } else {
              // Something happened in setting up the request
              return "Error setting up the request. Please try again.";
            }
          }
          
          return "An unexpected error occurred. Please try again.";
        })(),
        sender: 'ai',
        timestamp: new Date().toISOString(),
        type: 'error'
      };

      setMessages(prevMessages => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Debugging method to log all messages
  useEffect(() => {
    console.log('Current Messages:', messages);
  }, [messages]);

  return (
    <div className="chat-page">
      <ChatHeader onBack={() => navigate('/')} />
      <div className="chat-container">
        <ChatMessages 
          messages={messages} 
          isLoading={isLoading}
          messagesEndRef={messagesEndRef}
        />
        <ChatInput 
          onSendMessage={handleSendMessage} 
          isLoading={isLoading}
        />
      </div>
    </div>
  );
};

export default ChatPage;
