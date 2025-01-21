import React from 'react';
import { FaRobot, FaUser } from 'react-icons/fa';

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'ai';
  timestamp: string;
  type?: 'text' | 'code' | 'error';
}

interface ChatMessagesProps {
  messages: Message[];
  isLoading: boolean;
  messagesEndRef: React.RefObject<HTMLDivElement>;
}

const ChatMessages: React.FC<ChatMessagesProps> = ({ 
  messages, 
  isLoading, 
  messagesEndRef 
}) => {
  const renderMessageContent = (message: Message) => {
    switch (message.type) {
      case 'code':
        return (
          <pre className="code-block">
            <code>{message.content}</code>
          </pre>
        );
      case 'error':
        return <div className="error-message">{message.content}</div>;
      default:
        return <p>{message.content}</p>;
    }
  };

  return (
    <div className="chat-messages-container">
      {messages.map((message) => (
        <div 
          key={message.id} 
          className={`message ${message.sender}`}
        >
          <div className="message-avatar">
            {message.sender === 'ai' ? <FaRobot /> : <FaUser />}
          </div>
          <div className={`message-content ${message.type || 'text'}`}>
            {renderMessageContent(message)}
            <span className="message-timestamp">
              {new Date(message.timestamp).toLocaleTimeString()}
            </span>
          </div>
        </div>
      ))}
      
      {isLoading && (
        <div className="typing-indicator">
          <div className="typing-dot"></div>
          <div className="typing-dot"></div>
          <div className="typing-dot"></div>
          <span>AI is typing...</span>
        </div>
      )}
      
      <div ref={messagesEndRef} />
    </div>
  );
};

export default ChatMessages;
