# 🚀 Quick Setup Guide

## Prerequisites
- Python 3.9 or higher
- Ollama installed ([Download](https://ollama.com/download))
- Groq API Key ([Get one here](https://console.groq.com))

## Setup in 5 Steps

### 1️⃣ Install Ollama & Pull Model
```bash
# Install Ollama from https://ollama.com/download
# Then pull the embedding model:
ollama pull nomic-embed-text

# Start Ollama server:
ollama serve
```

### 2️⃣ Install Python Dependencies
```bash
cd rag-chatbot
pip install -r requirements.txt
```

### 3️⃣ Configure Environment
```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your Groq API key:
# GROQ_API_KEY=your_actual_api_key_here
```

### 4️⃣ Run the Application

**Linux/Mac:**
```bash
./start.sh
```

**Windows:**
```cmd
start.bat
```

**Manual Start:**
```bash
cd backend
python main.py
```

### 5️⃣ Access the App
Open your browser: **http://localhost:8000**

API docs: **http://localhost:8000/docs**

---

## What's New? ✨

### Fixed Issues
✅ **PDF Upload Fixed** - Proper file validation and error handling  
✅ **Modular Structure** - Clean separation of concerns  
✅ **Better Error Messages** - Clear feedback on what went wrong  
✅ **Session Management** - Improved session handling  

### New Features
🎨 **Modern UI** - Professional gradient design with animations  
📱 **Responsive** - Works on desktop, tablet, and mobile  
🔔 **Toast Notifications** - Beautiful status messages  
💬 **Better Chat** - Typing indicators and smooth scrolling  
📊 **Session Info Panel** - Track your session status  
🔄 **Drag & Drop** - Easy PDF upload  

### Backend Improvements
- **Modular Architecture** - Separated into services, routes, models
- **Better Validation** - Pydantic models for all requests
- **Logging** - Comprehensive logging throughout
- **Error Handling** - Proper exception handling and messages
- **Type Hints** - Full type annotations
- **Documentation** - Auto-generated API docs

### Frontend Improvements
- **Modern CSS** - CSS variables, flexbox, grid
- **Vanilla JS** - No framework dependencies
- **Accessibility** - Semantic HTML and ARIA labels
- **Animations** - Smooth transitions and effects
- **File Upload** - Drag & drop with visual feedback

---

## Project Structure

```
rag-chatbot/
├── 📱 frontend/              # Modern web interface
│   ├── index.html           # Main HTML
│   ├── style.css            # Modern styling
│   └── script.js            # Frontend logic
│
├── ⚙️ backend/              # FastAPI backend
│   ├── main.py             # App entry point
│   ├── config.py           # Configuration
│   ├── api/
│   │   └── routes.py       # API endpoints
│   ├── services/
│   │   ├── vector_service.py   # Vector store
│   │   └── chat_service.py     # Chat logic
│   ├── models/
│   │   └── schemas.py      # Data models
│   └── utils/
│       └── helpers.py      # Utilities
│
├── 📄 README.md            # Full documentation
├── 📋 requirements.txt     # Dependencies
├── 🔧 .env.example        # Config template
├── 🚀 start.sh            # Linux/Mac startup
└── 🚀 start.bat           # Windows startup
```

---

## Troubleshooting

### "Could not connect to Ollama"
**Solution:** Make sure Ollama is running:
```bash
ollama serve
```

### "Upload failed"
**Solutions:**
- Check file is a PDF (not scanned image)
- Ensure file is under 10MB
- Make sure PDF is not password-protected

### Port 8000 in use
**Solution:** Change port in .env:
```
PORT=8001
```

### No response from chat
**Solutions:**
- Verify Groq API key is correct
- Check internet connection
- Look at backend terminal for errors

---

## Usage Tips

1. **Upload First** - Always upload a PDF before chatting
2. **Clear History** - Use "Clear History" to reset conversation
3. **New Session** - Start fresh with "New Session"
4. **Ask Specific Questions** - More specific = better answers
5. **Check Sources** - Review cited pages for verification

---

## Next Steps

- ✅ Upload a test PDF
- ✅ Ask questions about the document
- ✅ Try clearing history
- ✅ Start a new session with different document
- ✅ Check out API docs at /docs
- ✅ Explore the modular code structure

---

**Need Help?** Check the full README.md for detailed documentation!
