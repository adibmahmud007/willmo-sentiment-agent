# 🤖 Willmo Chat - AI Chatbot with Voice & Emotional Intelligence

A sophisticated AI chatbot system with **voice input**, **JSON-based memory**, and **emotional intelligence** capabilities. Built with FastAPI and powered by Groq's lightning-fast LLM and Whisper APIs.

## ✨ Features

### 🎤 **Voice & Text Chat**
- **Text Chat**: Real-time text-based conversations
- **Voice Chat**: Upload audio files for speech-to-text processing
- **Multi-format Support**: MP3, WAV, M4A, WebM, and more
- **Real-time Transcription**: Powered by Groq Whisper API

### 🧠 **Smart Memory System**
- **JSON-based Storage**: Complete conversation history preserved
- **User-wise Memory**: Individual memory for each user
- **Context Awareness**: AI remembers previous conversations
- **Memory Optimization**: Automatic archiving of old conversations

### 💝 **Emotional Intelligence** *(Coming Soon)*
- **Emotion Detection**: Real-time emotion analysis from text/voice
- **Positivity Tracking**: Monitor mood patterns over time
- **Empathy-first Coaching**: Supportive and understanding responses
- **Personalized Guidance**: Tailored advice based on emotional context

### 🔧 **Developer Features**
- **Clean Architecture**: Modular route-based structure
- **RESTful API**: Well-documented endpoints
- **Auto Documentation**: Interactive API docs with Swagger UI
- **Comprehensive Logging**: Detailed request/response tracking
- **Error Handling**: Graceful error management

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Installation

1. **Clone or create the project structure:**
   ```bash
   # Use the PowerShell script (Windows)
   .\create_project.ps1
   
   # Or create manually
   mkdir willmo-chat && cd willmo-chat
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   # Create .env file
   echo "GROQ_API_KEY=your_groq_api_key_here" > .env
   ```

4. **Run the application:**
   ```bash
   python run.py
   ```

5. **Access the API:**
   - **API Base**: http://localhost:8000
   - **Documentation**: http://localhost:8000/docs
   - **Alternative Docs**: http://localhost:8000/redoc

## 📁 Project Structure

```
willmo-chat/
├── routes/                 # API route modules
│   ├── __init__.py
│   ├── chat_routes.py     # Chat & voice endpoints
│   ├── memory_routes.py   # Memory management
│   └── health_routes.py   # Health checks
├── models/                # Pydantic data models
│   ├── __init__.py
│   ├── chat_models.py     # Request/response models
│   └── memory_models.py   # Memory data structures
├── services/              # Business logic
│   ├── __init__.py
│   ├── chat_service.py    # Main chat processing
│   ├── groq_service.py    # Groq API integration
│   └── memory_service.py  # Memory management
├── utils/                 # Utility functions
│   ├── __init__.py
│   ├── helpers.py         # General utilities
│   └── transcript_audio.py # Audio transcription
├── main.py               # FastAPI application
├── config.py             # Configuration
├── run.py               # Application runner
├── requirements.txt     # Dependencies
└── .env                # Environment variables
```

## 🔗 API Endpoints

### Health Endpoints
- `GET /` - Basic health check
- `GET /health` - Detailed system status

### Chat Endpoints
- `POST /api/chat` - Text-based chat
- `POST /api/voice-chat` - Voice-based chat (file upload)

### Memory Endpoints
- `GET /api/memory/{user_id}` - Get user's memory
- `GET /api/conversations/{user_id}` - Full conversation history
- `DELETE /api/memory/{user_id}` - Clear user memory
- `GET /api/stats/{user_id}` - Memory statistics

## 💬 Usage Examples

### Text Chat
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "message": "Hello, how are you today?"
  }'
```

### Voice Chat
```bash
curl -X POST "http://localhost:8000/api/voice-chat" \
  -H "accept: application/json" \
  -F "user_id=user123" \
  -F "audio_file=@recording.mp3"
```

### Get User Memory
```bash
curl -X GET "http://localhost:8000/api/memory/user123"
```

## 📊 Response Examples

### Chat Response
```json
{
  "response": "Hello! I'm doing well, thank you for asking. How can I help you today?",
  "user_id": "user123",
  "timestamp": "2025-08-18T10:30:00.000Z",
  "memory_updated": true
}
```

### Voice Chat Response
```json
{
  "transcribed_text": "Hello, how are you today?",
  "ai_response": "Hello! I'm doing well, thank you for asking...",
  "user_id": "user123",
  "timestamp": "2025-08-18T10:30:00.000Z",
  "memory_updated": true,
  "transcription_success": true
}
```

### Memory Response
```json
{
  "user_id": "user123",
  "recent_conversations": [
    {
      "timestamp": "2025-08-18T10:30:00.000Z",
      "user_message": "Hello, how are you today?",
      "ai_response": "Hello! I'm doing well...",
      "message_type": "text",
      "transcribed_text": ""
    }
  ],
  "total_conversations": 5,
  "text_messages": 3,
  "voice_messages": 2,
  "last_updated": "2025-08-18T10:30:00.000Z"
}
```

## ⚙️ Configuration

### Environment Variables
```bash
# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional (defaults provided)
GROQ_MODEL=llama3-8b-8192
MAX_RECENT_MEMORIES=5
MAX_ARCHIVED_MEMORIES=10
```

### Supported Audio Formats
- **MP3** (.mp3)
- **WAV** (.wav) 
- **M4A** (.m4a)
- **MP4** (.mp4)
- **MPEG** (.mpeg)
- **MPGA** (.mpga)
- **WebM** (.webm)

### File Limits
- **Maximum file size**: 25MB
- **Transcription language**: Auto-detect (optimized for English)

## 🧠 Memory System

### How It Works
1. **Conversation Storage**: Each user-AI interaction stored as JSON
2. **Smart Filtering**: Trivial conversations filtered out automatically
3. **Memory Optimization**: Old conversations automatically archived
4. **Context Awareness**: AI accesses full conversation history for responses

### Memory Structure
```json
{
  "timestamp": "2025-08-18T10:30:00.000Z",
  "user_message": "What's the weather like?",
  "ai_response": "I don't have access to real-time weather...",
  "message_type": "text", // or "voice"
  "transcribed_text": "" // populated for voice messages
}
```

## 🔧 Development

### Adding New Routes
1. Create new route file in `routes/` directory
2. Import and include in `main.py`:
   ```python
   from routes import new_routes
   app.include_router(new_routes.router)
   ```

### Custom Configuration
Modify `config.py` to add new configuration options:
```python
class Config:
    # Add your custom configs here
    CUSTOM_SETTING = os.getenv("CUSTOM_SETTING", "default_value")
```

### Running in Development
```bash
# With auto-reload
python run.py

# Or with uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🚨 Error Handling

The system includes comprehensive error handling:

- **API Key Issues**: Clear messages for missing/invalid Groq API keys
- **File Validation**: Audio format and size validation
- **Rate Limiting**: Graceful handling of API rate limits
- **Transcription Errors**: Fallback responses for failed transcriptions
- **Memory Errors**: Safe handling of memory operations

## 📈 Performance

### Benchmarks
- **Text Response**: ~1-2 seconds
- **Voice Transcription**: ~2-4 seconds (depending on file size)
- **Memory Operations**: <100ms
- **Concurrent Users**: Supports multiple users simultaneously

### Optimization Tips
- Keep audio files under 10MB for faster processing
- Use MP3 format for best compression/quality balance
- Clear old memories periodically for optimal performance

## 🛡️ Security & Privacy

### Data Handling
- **In-Memory Storage**: No persistent database required
- **Session-based**: Data cleared on server restart
- **User Isolation**: Each user's data completely separate
- **No Data Persistence**: Conversations not permanently stored

### API Security
- **CORS Enabled**: Configurable for your domain
- **Input Validation**: All inputs validated before processing
- **Error Sanitization**: Sensitive errors not exposed to clients

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Add type hints where possible
- Include docstrings for new functions
- Add tests for new features

## 📞 Support

### Common Issues

**"API key not working"**
- Verify your Groq API key is correct
- Check .env file formatting
- Ensure no extra spaces in the key

**"Audio file upload fails"**
- Check file format is supported
- Verify file size is under 25MB
- Try converting to MP3 format

**"Memory not working"**
- Memory is in-memory only (clears on restart)
- Check user_id consistency across requests

### Getting Help
- Check the [API documentation](http://localhost:8000/docs)
- Review error logs in console output
- Verify all dependencies are installed correctly

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Groq**: For providing fast and reliable LLM and Whisper APIs
- **FastAPI**: For the excellent web framework
- **Pydantic**: For robust data validation
- **Uvicorn**: For the high-performance ASGI server

## 🔮 Roadmap

### Upcoming Features
- **Emotional Intelligence**: Real-time emotion detection and empathy-first coaching
- **Database Integration**: Optional persistent storage
- **User Authentication**: Secure user management
- **Real-time Chat**: WebSocket support for live conversations
- **Analytics Dashboard**: Usage and conversation analytics
- **Multi-language Support**: Support for multiple languages
- **Custom Models**: Integration with custom fine-tuned models

---

**Built with ❤️ for intelligent conversations**

For more information, visit our [documentation](http://localhost:8000/docs) or check out the [API reference](http://localhost:8000/redoc).
