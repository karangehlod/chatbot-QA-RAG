import React from 'react';
import { FaArrowLeft, FaRobot } from 'react-icons/fa';

interface ChatHeaderProps {
  onBack: () => void;
}

const ChatHeader: React.FC<ChatHeaderProps> = ({ onBack }) => {
  return (
    <div className="chat-header">
      <button className="back-button" onClick={onBack}>
        <FaArrowLeft />
      </button>
      <div className="chat-title">
        <FaRobot className="ai-icon" />
        <h2>AI Assistant</h2>
      </div>
    </div>
  );
};

export default ChatHeader;
