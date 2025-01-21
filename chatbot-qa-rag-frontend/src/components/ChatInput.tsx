import React, { useState, useRef, useEffect } from 'react';
import { FaPaperPlane, FaMicrophone } from 'react-icons/fa';
import '../styles/ChatPage.css'; // Add a CSS file for styling

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  isLoading: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({ 
  onSendMessage, 
  isLoading 
}) => {
  const [message, setMessage] = useState('');
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSubmit = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    
    const trimmedMessage = message.trim();
    if (trimmedMessage && !isLoading) {
      onSendMessage(trimmedMessage);
      setMessage('');
      inputRef.current?.focus();
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleVoiceInput = () => {
    if ('webkitSpeechRecognition' in window) {
      const recognition = new (window as any).webkitSpeechRecognition();
      recognition.lang = 'en-US';
      recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        setMessage(transcript);
        handleSubmit();
      };
      recognition.onerror = (event: any) => {
        console.error('Speech recognition error', event.error);
      };
      recognition.onend = () => {
        console.log('Speech recognition ended');
      };
      recognition.start();
    } else {
      alert('Speech recognition not supported in this browser');
    }
  };

  return (
    <form 
      className="chat-input-container" 
      onSubmit={handleSubmit}
    >
      <div className="input-wrapper">
        <textarea
          ref={inputRef}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message..."
          rows={1}
          disabled={isLoading}
        />
        <div className="input-actions">
          <button 
            type="button"
            onClick={handleVoiceInput}
            disabled={isLoading}
            className="voice-input"
          >
            <FaMicrophone />
          </button>
          <button 
            type="submit"
            disabled={!message.trim() || isLoading}
            className="send-message"
          >
            <FaPaperPlane />
          </button>
        </div>
      </div>
    </form>
  );
};

export default ChatInput;