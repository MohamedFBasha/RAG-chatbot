# 🤖 RAG Chatbot - AI Document Assistant

A modern, professional RAG (Retrieval-Augmented Generation) chatbot that allows you to upload PDF documents and have intelligent conversations about their content.

## ✨ Features

- 📄 **PDF Upload & Processing** - Upload any PDF document for analysis
- 💬 **Intelligent Chat** - Ask questions and get accurate answers from your documents
- 🧠 **Conversation Memory** - Maintains context throughout the conversation
- 📚 **Source Citations** - Shows which parts of the document were used for answers
- 🎨 **Modern UI** - Clean, professional interface with smooth animations
- 🔄 **Session Management** - Multiple sessions with independent chat histories
- ⚡ **Fast Retrieval** - Uses FAISS for efficient vector search
- 🌐 **RESTful API** - Well-documented API endpoints

## 🏗️ Architecture

```
rag-chatbot/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── api/
│   │   └── routes.py        # API endpoints
│   ├── services/
│   │   ├── vector_service.py    # Vector store management
│   │   └── chat_service.py      # Chat & RAG logic
│   ├── models/
│   │   └── schemas.py       # Pydantic models
│   └── utils/
│       └── helpers.py       # Utility functions
├── frontend/
│   ├── index.html          # Main HTML interface
│   ├── style.css           # Modern styling
│   └── script.js           # Frontend logic
└── requirements.txt        # Python dependencies
```

## 🚀 Quick Start

### Prerequisites

1. **Python 3.9+**
2. **Ollama** - For embeddings
3. **Groq API Key** - For LLM (get from [console.groq.com](https://console.groq.com))

### Installation

1. **Clone or download the project**
```bash
cd rag-chatbot
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Install and setup Ollama**
```bash
# Install Ollama (if not installed)
# Visit: https://ollama.com/download

# Pull the embedding model
ollama pull nomic-embed-text

# Start Ollama server
ollama serve
```

4. **Configure environment variables**
```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your API keys
GROQ_API_KEY=your_groq_api_key_here
HF_TOKEN=your_huggingface_token_here  # Optional
OLLAMA_BASE_URL=http://localhost:11434
```

5. **Run the application**
```bash
# From the backend directory
cd backend
python main.py
```

6. **Access the application**
Open your browser and navigate to:
```
http://localhost:8000
```

API documentation available at:
```
http://localhost:8000/docs
```

## 📖 Usage

### Using the Web Interface

1. **Start a Session**
   - The app automatically generates a session ID

2. **Upload a PDF**
   - Click the upload area or drag & drop a PDF file
   - Wait for processing (you'll see pages and chunks count)

3. **Start Chatting**
   - Type your question in the input box
   - Press Enter to send
   - Get AI-powered answers with source citations

4. **Manage Sessions**
   - **Clear History**: Removes chat messages but keeps the document
   - **New Session**: Starts fresh with a new document

### Using the API

#### Health Check
```bash
curl http://localhost:8000/api/health
```

#### Upload PDF
```bash
curl -X POST "http://localhost:8000/api/upload" \
  -F "file=@document.pdf" \
  -F "session_id=session_test123"
```

#### Send Chat Message
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is this document about?",
    "session_id": "session_test123"
  }'
```

#### Get Session Info
```bash
curl http://localhost:8000/api/sessions/session_test123/info
```

#### Clear Chat History
```bash
curl -X POST http://localhost:8000/api/sessions/session_test123/clear-history
```

#### Delete Session
```bash
curl -X DELETE http://localhost:8000/api/sessions/session_test123
```

## 🔧 Configuration

Edit `backend/config.py` to customize:

- **LLM Settings**: Model, temperature, max tokens
- **RAG Settings**: Chunk size, overlap, retrieval count
- **File Settings**: Max upload size, allowed extensions
- **Server Settings**: Host, port, CORS origins

## 🏢 Project Structure Details

### Backend Components

- **`main.py`**: FastAPI application setup and startup logic
- **`config.py`**: Centralized configuration using Pydantic Settings
- **`api/routes.py`**: All API endpoints with request/response handling
- **`services/vector_service.py`**: PDF processing and vector store management
- **`services/chat_service.py`**: RAG chain and conversation management
- **`models/schemas.py`**: Pydantic models for validation
- **`utils/helpers.py`**: Utility functions for file handling and validation

### Frontend Components

- **`index.html`**: Semantic HTML structure with accessibility features
- **`style.css`**: Modern CSS with CSS variables and responsive design
- **`script.js`**: Vanilla JavaScript for API interactions and UI updates

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern web framework
- **LangChain**: RAG orchestration
- **Groq**: Fast LLM inference (Llama 3)
- **Ollama**: Local embeddings (nomic-embed-text)
- **FAISS**: Efficient vector similarity search
- **PyPDF**: PDF text extraction

### Frontend
- **Vanilla JavaScript**: No framework dependencies
- **Modern CSS**: CSS Grid, Flexbox, Variables
- **Responsive Design**: Mobile-friendly interface

## 🐛 Troubleshooting

### PDF Upload Not Working

**Issue**: Upload fails or PDF processing errors

**Solutions**:
1. Check file size (must be < 10MB)
2. Ensure PDF is not password-protected
3. Verify PDF contains readable text (not scanned images)
4. Check backend logs for detailed errors

### Ollama Connection Issues

**Issue**: "Could not connect to Ollama" error

**Solutions**:
1. Verify Ollama is running: `ollama serve`
2. Check model is installed: `ollama list`
3. Pull model if missing: `ollama pull nomic-embed-text`
4. Verify `OLLAMA_BASE_URL` in `.env` file

### Chat Not Responding

**Issue**: Messages send but no response

**Solutions**:
1. Check Groq API key is valid
2. Verify session has uploaded PDF
3. Check backend logs for errors
4. Ensure internet connection for Groq API

### Port Already in Use

**Issue**: "Address already in use" error

**Solutions**:
1. Change port in `.env` file: `PORT=8001`
2. Or kill process using port 8000:
```bash
# Linux/Mac
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

## 📝 API Documentation

Full API documentation is available at `/docs` when the server is running.

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Serve frontend interface |
| GET | `/api/health` | Health check |
| POST | `/api/upload` | Upload PDF document |
| POST | `/api/chat` | Send chat message |
| GET | `/api/sessions/{id}/info` | Get session info |
| POST | `/api/sessions/{id}/clear-history` | Clear chat history |
| DELETE | `/api/sessions/{id}` | Delete session |
| GET | `/api/sessions` | List all sessions |

## 🔐 Security Notes

- Never commit `.env` file with real API keys
- Use environment variables for sensitive data
- Implement rate limiting for production
- Add authentication for multi-user environments
- Sanitize file uploads in production

## 🚀 Production Deployment

For production deployment:

1. **Set proper CORS origins** in `config.py`
2. **Use a production ASGI server**: Gunicorn with Uvicorn workers
3. **Add authentication** and rate limiting
4. **Use HTTPS** with proper SSL certificates
5. **Set up proper logging** and monitoring
6. **Configure firewall** rules
7. **Use a reverse proxy** (Nginx/Caddy)

Example production command:
```bash
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 📄 License

This project is provided as-is for educational and commercial use.

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📧 Support

For issues and questions:
- Check the troubleshooting section
- Review API documentation at `/docs`
- Check backend logs for detailed errors

## 🎯 Future Enhancements

- [ ] Support for multiple file formats (DOCX, TXT, etc.)
- [ ] User authentication and authorization
- [ ] Conversation export (PDF, JSON)
- [ ] Advanced filtering and search
- [ ] Real-time collaboration
- [ ] Mobile app
- [ ] Cloud storage integration
- [ ] Multiple language support

---

**Built with ❤️ using FastAPI, LangChain, and modern web technologies**
