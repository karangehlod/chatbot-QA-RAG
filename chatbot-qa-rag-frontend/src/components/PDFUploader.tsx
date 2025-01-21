import React, { useState, useEffect } from 'react';
import api from '../api';
import { useNavigate } from 'react-router-dom';
import { UploadStatus } from '../types'; // Import the UploadStatus type
import '../styles/App.css'; // Add a CSS file for styling

const PDFUploader: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<UploadStatus>({
    loading: false,
    success: false,
    error: null
  });
  const navigate = useNavigate();

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      const selectedFile = event.target.files[0];
      
      // Validate file type
      const allowedTypes = ['application/pdf', 'text/plain'];
      if (!allowedTypes.includes(selectedFile.type)) {
        setUploadStatus({
          loading: false,
          success: false,
          error: 'Please upload only PDF or TXT files'
        });
        return;
      }

      // Validate file size (e.g., max 10MB)
      const maxSize = 10 * 1024 * 1024; // 10MB
      if (selectedFile.size > maxSize) {
        setUploadStatus({
          loading: false,
          success: false,
          error: 'File size exceeds 10MB limit'
        });
        return;
      }

      setFile(selectedFile);
      setUploadStatus({ loading: false, success: false, error: null });
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    // Reset previous states
    setUploadStatus({ loading: true, success: false, error: null });

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await api.post('/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round(
            progressEvent.total ? (progressEvent.loaded * 100) / progressEvent.total : 0
          );
          console.log(`Upload progress: ${percentCompleted}%`);
        }
      });

      if (response.status === 202) {
        setUploadStatus({
          loading: false,
          success: true,
          error: null
        });

        // Short delay to show success state
        setTimeout(() => {
          navigate('/chat');
        }, 1000);
      } else {
        throw new Error('Unexpected response status');
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      setUploadStatus({
        loading: false,
        success: false,
        error: error instanceof Error 
          ? error.message 
          : 'An unexpected error occurred during upload'
      });
    }
  };

  return (
    <div className="upload-container">
      <div className="upload-wrapper">
        <h2>Upload a File</h2>
        
        {/* File Input */}
        <div className="file-input-container">
          <input 
            type="file" 
            id="file-upload"
            accept=".pdf,.txt"
            onChange={handleFileChange}
            className="file-input"
          />
          <label 
            htmlFor="file-upload" 
            className={`file-input-label ${file ? 'file-selected' : ''}`}
          >
            {file ? file.name : 'Choose File'}
          </label>
        </div>

        {/* Error Message */}
        {uploadStatus.error && (
          <div className="error-message">
            {uploadStatus.error}
          </div>
        )}

        {/* Upload Button */}
        
        <button 
          onClick={handleUpload} 
          disabled={!file || uploadStatus.loading}
          className={`upload-button ${
            uploadStatus.loading ? 'loading' : 
            uploadStatus.success ? 'success' : ''
          }`}
        >
          {uploadStatus.loading ? (
            <div className="spinner">
              <div className="bounce1"></div>
              <div className="bounce2"></div>
              <div className="bounce3"></div>
            </div>
          ) : uploadStatus.success ? (
            'Upload Successful!'
          ) : (
            'Upload File'
          )}
        </button>
      </div>
    </div>
  );
};

export default PDFUploader;
