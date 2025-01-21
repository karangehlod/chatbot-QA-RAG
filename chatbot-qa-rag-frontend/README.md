# React Frontend App

This project is a React-based frontend application that allows users to interact with a knowledge base through a chatbot interface and upload PDF documents.

## Features

- **PDF Upload**: Users can upload PDF documents to the knowledge base.
- **Chatbot Interface**: Users can ask questions in a chatbot-style interface and receive responses that may include relevant content from the uploaded documents.

## Getting Started

To get a local copy up and running, follow these steps:

### Prerequisites

- Node.js (version 14 or later)
- npm (version 5.6 or later)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd rag-chatbot-qa
   ```
3. Install the dependencies:
   ```bash
   npm install
   ```

### Running the Application

To start the application, run:
```bash
npm start
```
This will launch the app in your default web browser.

## Folder Structure

- `public/`: Contains static files like `index.html` and `manifest.json`.
- `src/`: Contains the React components and styles.
  - `components/`: Contains the `Chatbot.tsx` and `PDFUploader.tsx` components.
  - `styles/`: Contains the CSS styles for the application.
- `package.json`: Lists the project dependencies and scripts.
- `tsconfig.json`: TypeScript configuration file.
- `README.md`: Documentation for the project.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or features.

## License

This project is licensed under the MIT License.