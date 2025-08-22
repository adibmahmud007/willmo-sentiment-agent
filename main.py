from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Import route modules
from routes import chat_routes, memory_routes, health_routes

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Willmo Chat - Voice & Text Chatbot with JSON Memory",
    description="A chatbot system with voice input, JSON-based conversation memory using Groq API",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include route modules
app.include_router(health_routes.router)
app.include_router(chat_routes.router)
app.include_router(memory_routes.router)

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Willmo Chat API starting up...")
    logger.info("📱 Text & Voice chat endpoints ready")
    logger.info("🧠 JSON memory system active")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 Willmo Chat API shutting down...")

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")