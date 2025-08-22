import uvicorn

if __name__ == "__main__":
    print("🚀 Starting Text-based Chatbot with Memory...")
    print("📝 Make sure to set your GROQ_API_KEY in .env file")
    print("🌐 API will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    
    uvicorn.run(
        "main:app",  # Import string format
        host="0.0.0.0", 
        port=8000, 
        log_level="info",
        reload=True  # Auto-reload on code changes
    )