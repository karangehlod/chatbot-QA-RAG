import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import PDFUploader from './components/PDFUploader';
import Chatbot from './components/Chatbot';

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<PDFUploader />} />
        <Route path="/chat" element={<Chatbot />} />
      </Routes>
    </Router>
  );
};

export default App;