# chatbot-QA-RAG

Simple web application allowing users to upload content and receive answers based on the content. Utilizes Retrieval-Augmented Generation (RAG) to enhance the AI response.

## Tech Stack

- **Frontend**: React, TypeScript, Axios, React Router, React Icons
- **Backend**: Django, Django REST Framework, PostgreSQL
- **Database**: PostgreSQL with pgvector extension
- **Deployment**: Docker, Docker Compose

## Functionality

- **File Upload**: Users can upload PDF or text files.
- **Chat Interface**: Users can ask questions based on the uploaded content.
- **AI Response**: The backend uses Azure OpenAI to generate responses based on the provided context.

## Components

### Frontend

- **React**: For building the user interface.
- **TypeScript**: For type safety.
- **Axios**: For making HTTP requests to the backend.
- **React Router**: For navigation within the app.
- **React Icons**: For using icons in the UI.

### Backend

- **Django**: For building the backend API.
- **Django REST Framework**: For creating RESTful APIs.
- **PostgreSQL**: For storing data.
- **pgvector**: For vector similarity search.

### Database

- **PostgreSQL**: A powerful, open-source object-relational database system.
- **pgvector**: An extension for PostgreSQL that provides vector similarity search.

## Running the Project Locally

### Prerequisites

- Node.js and npm
- Python 3.9+
- PostgreSQL

### Backend Setup

1. **Navigate to the backend directory**:

    ```sh
    cd rag_chatbot
    ```

2. **Install Python dependencies**:

    ```sh
    pip install -r requirements.txt
    ```

3. **Set up the database**:

    ```sh
    python manage.py migrate
    ```

4. **Run the backend server**:

    ```sh
    python manage.py runserver
    ```

### Frontend Setup

1. **Navigate to the frontend directory**:

    ```sh
    cd chatbot-qa-rag-frontend
    ```

2. **Install Node.js dependencies**:

    ```sh
    npm install
    ```

3. **Run the frontend server**:

    ```sh
    npm start
    ```

### Running the Project with Docker

1. **Build and start the services**:

    ```sh
    docker-compose up --build
    ```

2. **Access the application**:

    - Frontend: [http://localhost:3000](http://localhost:3000)
    - Backend: [http://localhost:8000](http://localhost:8000)

## Sending Queries

### Uploading a File

1. **Navigate to the frontend application**: [http://localhost:3000](http://localhost:3000)
2. **Upload a PDF or text file**: Use the file upload interface to upload your content.

### Asking a Question

1. **Enter your question**: Use the chat interface to type your question based on the uploaded content.
2. **Send the question**: Click the send button or press Enter to submit your question.
3. **Receive the response**: The AI will process your question and provide a response based on the uploaded content.

## Testing

### Running Tests Locally

1. **Backend Tests**:

    ```sh
    cd rag_chatbot
    python manage.py test
    ```

2. **Frontend Tests**:

    ```sh
    cd chatbot-qa-rag-frontend
    npm test
    ```

### Running Tests with Docker

1. **Run backend tests**:

    ```sh
    docker-compose run backend python manage.py test
    ```

2. **Run frontend tests**:

    ```sh
    docker-compose run frontend npm test
    ```

## Authors

- **Author Name**: [Your Name](https://github.com/your-github-username)
- **Author Name**: [Collaborator Name](https://github.com/collaborator-github-username)

## License

This project is licensed under the MIT License - see the [LICENSE](http://_vscodecontentref_/1) file for details.