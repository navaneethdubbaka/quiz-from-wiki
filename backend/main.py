# main.py
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from datetime import datetime
import json
import os

# Import our modules
from database import get_db, init_db, Quiz
from models import QuizGenerateRequest, QuizGenerateResponse, QuizHistoryItem, ErrorResponse
from scraper import scrape_wikipedia
from llm_quiz_generator import generate_quiz, validate_quiz_output

# Database initialization flag
_db_initialized = False

def ensure_db_initialized():
    """Initialize database - called on startup"""
    global _db_initialized
    if not _db_initialized:
        try:
            init_db()
            _db_initialized = True
            print("✅ Database initialized")
        except Exception as e:
            print(f"⚠️ Database initialization warning: {e}")
            # Don't fail if DB init fails (might be connection issue)
            _db_initialized = True

# CORS origins - allow local dev and production deployments
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",") if origin.strip()]

# Log CORS configuration for debugging
print(f"🌐 CORS allowed origins: {allowed_origins}")

# Initialize FastAPI app with lifespan for database initialization
try:
    from contextlib import asynccontextmanager
    
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Startup: Initialize database
        ensure_db_initialized()
        yield
        # Shutdown: cleanup if needed
        pass
    
    app = FastAPI(
        title="AI Wiki Quiz Generator API",
        description="Generate educational quizzes from Wikipedia articles using AI",
        version="1.0.0",
        lifespan=lifespan
    )
except ImportError:
    # Fallback for older FastAPI versions
    app = FastAPI(
        title="AI Wiki Quiz Generator API",
        description="Generate educational quizzes from Wikipedia articles using AI",
        version="1.0.0"
    )
    
    @app.on_event("startup")
    def startup_event():
        """Initialize database tables on startup"""
        ensure_db_initialized()

# Configure CORS (allow frontend to communicate with backend)
# For production, allow all origins by default (can be restricted via ALLOWED_ORIGINS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if "*" in allowed_origins or not allowed_origins else allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
print(f"🌐 CORS: Allowing origins: {'* (all)' if '*' in allowed_origins or not allowed_origins else allowed_origins}")


# Add request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests for debugging"""
    # Handle OPTIONS preflight requests
    if request.method == "OPTIONS":
        response = await call_next(request)
        return response
    
    print(f"\n📥 {request.method} {request.url.path}")
    print(f"   Origin: {request.headers.get('origin', 'N/A')}")
    
    try:
        response = await call_next(request)
        print(f"✅ {request.method} {request.url.path} - Status: {response.status_code}")
        return response
    except Exception as e:
        print(f"❌ {request.method} {request.url.path} - Error: {str(e)}")
        raise


# Add validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors with detailed messages"""
    print(f"❌ Validation error on {request.method} {request.url.path}: {exc.errors()}")
    return JSONResponse(
        status_code=422,  # Use 422 for validation errors (FastAPI standard)
        content={
            "detail": "Request validation failed",
            "errors": exc.errors(),
            "body": str(exc.body) if hasattr(exc, 'body') else None
        }
    )


# Handle OPTIONS requests explicitly (CORS preflight)
@app.options("/{full_path:path}")
async def options_handler(full_path: str):
    """Handle CORS preflight OPTIONS requests"""
    return JSONResponse(
        status_code=200,
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Max-Age": "3600",
        }
    )


# Root endpoint
@app.get("/")
def root():
    """Root endpoint - API status"""
    return {
        "message": "AI Wiki Quiz Generator API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "generate_quiz": "POST /generate_quiz",
            "get_history": "GET /history",
            "get_quiz": "GET /quiz/{quiz_id}"
        }
    }


# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


# Database test endpoint
@app.get("/test-db")
def test_database(db: Session = Depends(get_db)):
    """Test database connection and return status"""
    try:
        # Ensure database is initialized
        ensure_db_initialized()
        
        # Try to query the database
        from database import engine, DATABASE_URL
        from sqlalchemy import text
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
        
        # Try to query Quiz table (might not exist yet)
        try:
            quiz_count = db.query(Quiz).count()
            return {
                "status": "success",
                "database_type": "PostgreSQL" if DATABASE_URL.startswith("postgresql") else "SQLite",
                "connection": "ok",
                "tables_created": True,
                "quiz_count": quiz_count,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            # Tables might not be created yet
            return {
                "status": "success",
                "database_type": "PostgreSQL" if DATABASE_URL.startswith("postgresql") else "SQLite",
                "connection": "ok",
                "tables_created": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "database_type": "PostgreSQL" if os.getenv("DATABASE_URL", "").startswith("postgresql") else "SQLite",
            "timestamp": datetime.utcnow().isoformat()
        }


# Endpoint 1: Generate Quiz
@app.post("/generate_quiz", response_model=QuizGenerateResponse)
def generate_quiz_endpoint(request: QuizGenerateRequest, db: Session = Depends(get_db)):
    """
    Generate a quiz from a Wikipedia article URL.
    
    Args:
        request: QuizGenerateRequest containing the Wikipedia URL
        db: Database session
        
    Returns:
        QuizGenerateResponse with the generated quiz data
    """
    # Ensure database is initialized
    ensure_db_initialized()
    try:
        # Validate request
        if not request.url:
            raise HTTPException(status_code=400, detail="URL is required")
        
        url = request.url.strip()
        
        if not url:
            raise HTTPException(status_code=400, detail="URL cannot be empty")
        
        print(f"\n{'='*80}")
        print(f"📥 Received request to generate quiz for: {url}")
        print(f"{'='*80}")
        
        # Check if URL already exists in database
        existing_quiz = db.query(Quiz).filter(Quiz.url == url).first()
        if existing_quiz:
            print(f"♻️ Quiz already exists for this URL (ID: {existing_quiz.id})")
            print(f"   Returning cached quiz...")
            
            # Parse the stored JSON data
            quiz_data = json.loads(existing_quiz.full_quiz_data)
            
            return QuizGenerateResponse(
                id=existing_quiz.id,
                url=existing_quiz.url,
                title=existing_quiz.title,
                date_generated=existing_quiz.date_generated.isoformat(),
                summary=quiz_data['summary'],
                key_entities=quiz_data['key_entities'],
                sections=quiz_data['sections'],
                quiz=quiz_data['quiz'],
                related_topics=quiz_data['related_topics']
            )
        
        # Step 1: Scrape Wikipedia
        print("\n🕷️ Step 1: Scraping Wikipedia article...")
        scrape_result = scrape_wikipedia(url)
        
        if scrape_result['error']:
            print(f"❌ Scraping failed: {scrape_result['error']}")
            raise HTTPException(status_code=400, detail=scrape_result['error'])
        
        title = scrape_result['title']
        content = scrape_result['content']
        
        print(f"✅ Article scraped successfully!")
        print(f"   Title: {title}")
        print(f"   Content length: {len(content)} characters")
        
        # Step 2: Generate Quiz with LLM
        print("\n🤖 Step 2: Generating quiz with AI...")
        quiz_result = generate_quiz(title, content)
        
        if not quiz_result['success']:
            print(f"❌ Quiz generation failed: {quiz_result['error']}")
            raise HTTPException(status_code=500, detail=f"Quiz generation failed: {quiz_result['error']}")
        
        quiz_data = quiz_result['data']
        
        # Step 3: Validate Quiz Output
        print("\n✅ Step 3: Validating quiz...")
        is_valid, error_msg = validate_quiz_output(quiz_data)
        
        if not is_valid:
            print(f"❌ Validation failed: {error_msg}")
            raise HTTPException(status_code=500, detail=f"Quiz validation failed: {error_msg}")
        
        print("✅ Quiz validation passed!")
        
        # Step 4: Save to Database
        print("\n💾 Step 4: Saving to database...")
        new_quiz = Quiz(
            url=url,
            title=title,
            scraped_content=content,  # Store original content
            full_quiz_data=json.dumps(quiz_data)  # Convert dict to JSON string
        )
        
        db.add(new_quiz)
        db.commit()
        db.refresh(new_quiz)
        
        print(f"✅ Quiz saved to database with ID: {new_quiz.id}")
        print(f"{'='*80}\n")
        
        # Return response
        return QuizGenerateResponse(
            id=new_quiz.id,
            url=new_quiz.url,
            title=new_quiz.title,
            date_generated=new_quiz.date_generated.isoformat(),
            summary=quiz_data['summary'],
            key_entities=quiz_data['key_entities'],
            sections=quiz_data['sections'],
            quiz=quiz_data['quiz'],
            related_topics=quiz_data['related_topics']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Endpoint 2: Get Quiz History
@app.get("/history", response_model=list[QuizHistoryItem])
def get_history(db: Session = Depends(get_db)):
    """
    Get a list of all generated quizzes.
    
    Args:
        db: Database session
        
    Returns:
        List of QuizHistoryItem objects
    """
    # Ensure database is initialized
    ensure_db_initialized()
    try:
        print("\n📚 Fetching quiz history...")
        
        # Query all quizzes, ordered by most recent first
        quizzes = db.query(Quiz).order_by(Quiz.date_generated.desc()).all()
        
        print(f"✅ Found {len(quizzes)} quiz(zes) in history")
        
        # Convert to response model
        history = [
            QuizHistoryItem(
                id=quiz.id,
                url=quiz.url,
                title=quiz.title,
                date_generated=quiz.date_generated.isoformat()
            )
            for quiz in quizzes
        ]
        
        return history
        
    except Exception as e:
        print(f"❌ Error fetching history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch history: {str(e)}")


# Endpoint 3: Get Specific Quiz by ID
@app.get("/quiz/{quiz_id}", response_model=QuizGenerateResponse)
def get_quiz_by_id(quiz_id: int, db: Session = Depends(get_db)):
    """
    Get a specific quiz by its ID.
    
    Args:
        quiz_id: ID of the quiz to retrieve
        db: Database session
        
    Returns:
        QuizGenerateResponse with the quiz data
    """
    # Ensure database is initialized
    ensure_db_initialized()
    try:
        print(f"\n🔍 Fetching quiz with ID: {quiz_id}")
        
        # Query quiz by ID
        quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
        
        if not quiz:
            print(f"❌ Quiz not found with ID: {quiz_id}")
            raise HTTPException(status_code=404, detail=f"Quiz with ID {quiz_id} not found")
        
        print(f"✅ Quiz found: {quiz.title}")
        
        # Deserialize the JSON data
        quiz_data = json.loads(quiz.full_quiz_data)
        
        # Return response
        return QuizGenerateResponse(
            id=quiz.id,
            url=quiz.url,
            title=quiz.title,
            date_generated=quiz.date_generated.isoformat(),
            summary=quiz_data['summary'],
            key_entities=quiz_data['key_entities'],
            sections=quiz_data['sections'],
            quiz=quiz_data['quiz'],
            related_topics=quiz_data['related_topics']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error fetching quiz: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch quiz: {str(e)}")


# Endpoint 4: Delete Quiz (Bonus - for testing)
@app.delete("/quiz/{quiz_id}")
def delete_quiz(quiz_id: int, db: Session = Depends(get_db)):
    """
    Delete a quiz by ID (useful for testing).
    
    Args:
        quiz_id: ID of the quiz to delete
        db: Database session
        
    Returns:
        Success message
    """
    try:
        print(f"\n🗑️ Deleting quiz with ID: {quiz_id}")
        
        quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
        
        if not quiz:
            raise HTTPException(status_code=404, detail=f"Quiz with ID {quiz_id} not found")
        
        db.delete(quiz)
        db.commit()
        
        print(f"✅ Quiz deleted successfully")
        
        return {"message": f"Quiz {quiz_id} deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error deleting quiz: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete quiz: {str(e)}")


# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)