# main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
import json

# Import our modules
from database import get_db, init_db, Quiz
from models import QuizGenerateRequest, QuizGenerateResponse, QuizHistoryItem, ErrorResponse
from scraper import scrape_wikipedia
from llm_quiz_generator import generate_quiz, validate_quiz_output

# Initialize FastAPI app
app = FastAPI(
    title="AI Wiki Quiz Generator API",
    description="Generate educational quizzes from Wikipedia articles using AI",
    version="1.0.0"
)

# CORS origins - allow local dev and Vercel deployments
import os
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

# Add Vercel URL if available
if os.getenv("VERCEL_URL"):
    vercel_url = f"https://{os.getenv('VERCEL_URL')}"
    if vercel_url not in allowed_origins:
        allowed_origins.append(vercel_url)

# Configure CORS (allow frontend to communicate with backend)
# In Vercel, we allow all origins since frontend and backend are on same domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if os.getenv("VERCEL") else allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    """Initialize database tables on startup"""
    init_db()
    print("✅ Database initialized")


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
    try:
        url = request.url.strip()
        
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