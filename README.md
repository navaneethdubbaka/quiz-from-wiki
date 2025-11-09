# AI Wiki Quiz Generator

A full-stack application that transforms Wikipedia articles into engaging, AI-powered educational quizzes using FastAPI, React, PostgreSQL, and Google's Gemini AI.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Sample Data](#sample-data)
- [Screenshots](#screenshots)
- [Prompt Engineering](#prompt-engineering)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)

---

## ✨ Features

### Core Functionality
- **Smart Web Scraping**: Extracts clean, structured content from Wikipedia articles using BeautifulSoup
- **AI-Powered Quiz Generation**: Leverages Google Gemini AI via LangChain to create 5-10 high-quality questions
- **Comprehensive Quiz Data**: Includes summaries, key entities, article sections, and related topics
- **Dual Quiz Modes**: 
- **View Mode**: See all answers and explanations immediately
- **Take Quiz Mode**: Interactive quiz experience with scoring
- **Persistent Storage**: PostgreSQL database stores all quizzes with full retrieval capability
- **Quiz History**: Browse and revisit all previously generated quizzes
- **Smart Caching**: Prevents duplicate scraping of the same URL

### Advanced Features
- **Structured Output Validation**: Pydantic schemas ensure consistent, high-quality quiz data
- **Difficulty Levels**: Questions categorized as easy, medium, or hard
- **Rich Explanations**: Each question includes context-grounded explanations
- **Entity Extraction**: Automatically identifies people, organizations, and locations
- **Related Topics**: Suggests relevant Wikipedia articles for further learning
- **URL Validation**: Client and server-side validation for Wikipedia URLs
- **Error Handling**: Graceful handling of network errors, invalid URLs, and API failures
- **Responsive UI**: Clean, modern interface built with React and CSS

---

## 🛠️ Tech Stack

### Backend
- **Python 3.10+**: Core programming language
- **FastAPI**: High-performance web framework
- **SQLAlchemy**: ORM for database operations
- **PostgreSQL**: Production-grade relational database
- **BeautifulSoup4**: HTML parsing and web scraping
- **LangChain**: LLM application framework
- **Pydantic**: Data validation and settings management
- **Google Gemini AI**: Large language model for quiz generation

### Frontend
- **React 18**: UI library
- **Axios**: HTTP client
- **Modern CSS**: Custom styling with CSS variables

### Development Tools
- **Uvicorn**: ASGI server
- **python-dotenv**: Environment variable management

---

## 📁 Project Structure

```
ai-quiz-generator/
├── backend/
│   ├── venv/                       # Python virtual environment
│   ├── database.py                 # Database setup and Quiz model
│   ├── models.py                   # Pydantic schemas for API
│   ├── scraper.py                  # Wikipedia scraping logic
│   ├── llm_quiz_generator.py       # LLM integration and prompt templates
│   ├── main.py                     # FastAPI app and endpoints
│   ├── requirements.txt            # Python dependencies
│   ├── .env                        # Environment variables (not in repo)
│   └── testing/                    # Testing phase
│   └── sample_outputs/             # JSON responses from API
│       ├── alan_turing.json
│       ├── artificial_intelligence.json
│       └── world_war_ii.json
│
├── frontend/
│   ├── public/                     # Static assets
│   ├── src/
│   │   ├── components/
│   │   │   ├── CollapseSection.jsx # Section Collapse component
│   │   │   ├── HistoryTable.jsx    # Quiz history table component
│   │   │   ├── Modal.jsx           # Reusable modal component
│   │   │   └── QuizDisplay.jsx     # Quiz rendering component
│   │   ├── services/
│   │   │   └── api.js              # API communication layer
│   │   ├── tabs/
│   │   │   ├── GenerateQuizTab.jsx # Quiz generation UI
│   │   │   └── HistoryTab.jsx      # History view UI
│   │   ├── App.jsx                 # Main application component
│   │   └── index.css               # Global styles
│   ├── package.json                # Node.js dependencies
│   └── vite.config.js              # Vite configuration
│
│
├── screenshots/                    # Application screenshots
│   ├── 01_generate_quiz.png
│   ├── 02_loading_state.png
│   ├── 03_quiz_display.png
│   ├── 04_take_quiz_mode.png
│   ├── 05_history_view.png
│   └── 06_details_modal.png
│
└── README.md                       # This file
```

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10 or higher** ([Download](https://www.python.org/downloads/))
- **PostgreSQL 13 or higher** ([Download](https://www.postgresql.org/download/))
- **Node.js 16+ and npm** ([Download](https://nodejs.org/))
- **Git** ([Download](https://git-scm.com/downloads))
- **Google Gemini API Key** ([Get one here](https://makersuite.google.com/app/apikey))

---

## 🚀 Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/ai-quiz-generator.git
cd ai-quiz-generator
```

### Step 2: Backend Setup

#### 2.1 Navigate to Backend Directory

```bash
cd backend
```

#### 2.2 Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 2.3 Install Dependencies

```bash
pip install -r requirements.txt
```

#### 2.4 Setup PostgreSQL Database

**Option A: Using psql command line**

```bash
# Login to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE quiz_generator_db;

# Exit
\q
```

**Option B: Using pgAdmin**
1. Open pgAdmin
2. Right-click on "Databases"
3. Select "Create" → "Database"
4. Name it `quiz_generator_db`
5. Click "Save"

#### 2.5 Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
# Copy example file
cp .env.example .env

# Edit .env with your credentials
```

**`.env` file contents:**

```env
# Gemini API Key (Required)
GEMINI_API_KEY=your_gemini_api_key_here

# Database Configuration
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=quiz_generator_db
```

#### 2.6 Initialize Database

```bash
python -c "from database import init_db; init_db()"
```

You should see: `✅ Database tables created successfully!`

### Step 3: Frontend Setup

#### 3.1 Navigate to Frontend Directory

```bash
cd ../frontend
```

#### 3.2 Install Dependencies

```bash
npm install
```

---

## ⚙️ Configuration

### Backend Configuration

**Database Settings** (`backend/.env`):
```env
DB_USER=postgres          # Your PostgreSQL username
DB_PASSWORD=yourpassword  # Your PostgreSQL password
DB_HOST=localhost         # Database host
DB_PORT=5432              # PostgreSQL port
DB_NAME=quiz_generator_db # Database name
```

**API Settings** (`backend/main.py`):
- **Port**: 8000 (default)
- **CORS**: Configured for `http://localhost:5173` (Vite default)
- **Timeout**: 120 seconds for quiz generation

### Frontend Configuration

**API Base URL** (`frontend/src/services/api.js`):
```javascript
const API_BASE_URL = 'http://localhost:8000';
```

**Development Server** (`frontend/vite.config.js`):
- **Port**: 5173 (Vite default)
- **Host**: localhost

---

## 🎮 Running the Application

### Start Backend Server

```bash
# Activate virtual environment (if not already active)
cd backend
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Run FastAPI server
python main.py
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
✅ Database initialized
```

**Backend will be available at:** `http://localhost:8000`

### Start Frontend Development Server

Open a **new terminal** window:

```bash
cd frontend
npm run dev
```

**Expected output:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

**Frontend will be available at:** `http://localhost:5173`

### Access the Application

Open your browser and navigate to:
```
http://localhost:5173
```

---

## 🔌 API Endpoints

### Base URL
```
http://localhost:8000
```

### Endpoints Overview

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| GET | `/` | API status and info | None | API information |
| GET | `/health` | Health check | None | Health status |
| POST | `/generate_quiz` | Generate quiz from URL | `{"url": "..."}` | Full quiz data |
| GET | `/history` | Get all quiz history | None | Array of quiz items |
| GET | `/quiz/{quiz_id}` | Get specific quiz | None | Full quiz data |
| DELETE | `/quiz/{quiz_id}` | Delete quiz (testing) | None | Success message |

### Detailed Endpoint Documentation

#### 1. Generate Quiz

**POST** `/generate_quiz`

Generates a quiz from a Wikipedia article URL.

**Request:**
```json
{
  "url": "https://en.wikipedia.org/wiki/Alan_Turing"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "url": "https://en.wikipedia.org/wiki/Alan_Turing",
  "title": "Alan Turing",
  "date_generated": "2024-01-15T10:30:00",
  "summary": "Alan Turing was a British mathematician and computer scientist...",
  "key_entities": {
    "people": ["Alan Turing", "Alonzo Church"],
    "organizations": ["University of Cambridge", "Bletchley Park"],
    "locations": ["United Kingdom", "Princeton"]
  },
  "sections": ["Early life", "Education", "World War II", "Legacy"],
  "quiz": [
    {
      "question": "Where did Alan Turing study?",
      "options": [
        "Harvard University",
        "Cambridge University",
        "Oxford University",
        "Princeton University"
      ],
      "answer": "Cambridge University",
      "difficulty": "easy",
      "explanation": "Alan Turing studied at King's College, Cambridge."
    }
  ],
  "related_topics": ["Cryptography", "Enigma machine", "Computer science"]
}
```

**Error Response (400 Bad Request):**
```json
{
  "detail": "Invalid Wikipedia URL. Please provide a valid Wikipedia article URL."
}
```

#### 2. Get Quiz History

**GET** `/history`

Retrieves all generated quizzes.

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "url": "https://en.wikipedia.org/wiki/Alan_Turing",
    "title": "Alan Turing",
    "date_generated": "2024-01-15T10:30:00"
  },
  {
    "id": 2,
    "url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "title": "Artificial intelligence",
    "date_generated": "2024-01-15T11:45:00"
  }
]
```

#### 3. Get Quiz by ID

**GET** `/quiz/{quiz_id}`

Retrieves a specific quiz by its ID.

**Response (200 OK):** Same as Generate Quiz response

**Error Response (404 Not Found):**
```json
{
  "detail": "Quiz with ID 999 not found"
}
```

---

## 🧪 Testing

### Manual Testing Steps

#### Test 1: Generate Quiz (Tab 1)

1. **Start both servers** (backend and frontend)
2. **Navigate to Generate Quiz tab**
3. **Enter a Wikipedia URL**:
   ```
   https://en.wikipedia.org/wiki/Alan_Turing
   ```
4. **Click "Generate Quiz"**
5. **Wait 30-60 seconds** for processing
6. **Verify the output contains**:
   - Article summary
   - Key entities (people, organizations, locations)
   - Article sections
   - 5-10 quiz questions with explanations
   - Related topics
7. **Test "Take Quiz" mode**:
   - Click "🎮 Take Quiz Mode"
   - Select answers for all questions
   - Click "Submit Quiz"
   - Verify score calculation and feedback

#### Test 2: View History (Tab 2)

1. **Navigate to Quiz History tab**
2. **Verify table shows** all generated quizzes
3. **Click "Details"** on any quiz
4. **Verify modal opens** with full quiz data
5. **Test modal interactions**:
   - Scroll through quiz
   - Close modal (X button or ESC key)
   - Reopen with different quiz

#### Test 3: Caching

1. **Generate quiz** for a URL (e.g., Alan Turing)
2. **Generate again** with same URL
3. **Verify instant response** (cached)
4. **Check console logs** for "Quiz already exists" message

#### Test 4: Error Handling

Test invalid inputs:
```
# Invalid URL
http://example.com

# Non-Wikipedia URL
https://google.com

# Non-existent Wikipedia page
https://en.wikipedia.org/wiki/ThisPageDoesNotExist123456
```

Verify appropriate error messages are displayed.

### API Testing with cURL

#### Test Health Endpoint

```bash
curl http://localhost:8000/health
```

#### Test Generate Quiz

```bash
curl -X POST http://localhost:8000/generate_quiz \
  -H "Content-Type: application/json" \
  -d '{"url": "https://en.wikipedia.org/wiki/Python_(programming_language)"}'
```

#### Test Get History

```bash
curl http://localhost:8000/history
```

#### Test Get Quiz by ID

```bash
curl http://localhost:8000/quiz/1
```

---

## 📦 Sample Data

Sample Wikipedia URLs are provided in `sample_data/test_urls.txt`:

### Recommended Test URLs

```
    https://en.wikipedia.org/wiki/Artificial_intelligence",
    "https://en.wikipedia.org/wiki/Climate_change",
    "https://en.wikipedia.org/wiki/Albert_Einstein",
    "https://en.wikipedia.org/wiki/World_War_II",
    "https://en.wikipedia.org/wiki/Photosynthesis",
    "https://en.wikipedia.org/wiki/Renaissance",
     "https://en.wikipedia.org/wiki/Machine_learning",
    "https://en.wikipedia.org/wiki/Elon_Musk"

```

### Sample JSON Outputs

Full JSON responses for these URLs are available in `backend/sample_outputs/`:
- `alan_turing.json`
- `artificial_intelligence.json`
- `world_war_ii.json`

---

## 📸 Screenshots

Screenshots demonstrating all features are available in the `screenshots/` directory:


## 🎯 Prompt Engineering

### LLM Prompt Template

The system uses a carefully crafted prompt template to ensure high-quality quiz generation:

**Location:** `backend/llm_quiz_generator.py`

```python
template = """You are a quiz generation system. You must return ONLY a single valid JSON object, nothing else.

Article Title: {title}

Article Content:
{content}

Generate a quiz with 5-7 questions in this EXACT format (copy this structure exactly):

{{
  "summary": "Write a 2-3 sentence summary of the article here",
  "key_entities": {{
    "people": ["List important people mentioned"],
    "organizations": ["List important organizations"],
    "locations": ["List important locations"]
  }},
  "sections": ["List main section titles from article"],
  "quiz": [
    {{
      "question": "Write question here?",
      "options": ["First option", "Second option", "Third option", "Fourth option"],
      "answer": "First option",
      "difficulty": "easy",
      "explanation": "Explain why this answer is correct based on the article"
    }}
  ],
  "related_topics": ["Related topic 1", "Related topic 2", "Related topic 3", "Related topic 4", "Related topic 5"]
}}

CRITICAL RULES:
- Return ONLY the JSON object above with your content filled in
- Generate 5-7 questions total
- Each question MUST have exactly 4 options
- The "answer" field MUST exactly match one of the options
- Difficulty must be "easy", "medium", or "hard"
- Do NOT write anything before the JSON
- Do NOT write anything after the JSON
- Do NOT create multiple JSON objects
- Make sure all JSON is valid (proper quotes, commas, brackets)

Return the JSON now:"""
```

### Key Prompt Design Principles

1. **Grounding**: Explicitly requires all content to be based on the article
2. **Anti-Hallucination**: Multiple warnings against inventing information
3. **Quality Guidelines**: Specific criteria for difficulty distribution and question types
4. **Structured Output**: JSON schema enforcement via Pydantic
5. **Comprehension Focus**: Emphasis on understanding over rote memorization
6. **Contextual Explanations**: Requires explanations tied to article sections

### Output Validation

Pydantic schemas ensure consistent structure:

```python
class QuizQuestion(BaseModel):
    question: str
    options: List[str]  # Exactly 4 options
    answer: str         # Must be one of the options
    difficulty: str     # Must be: easy, medium, or hard
    explanation: str

class QuizOutput(BaseModel):
    summary: str
    key_entities: KeyEntities
    sections: List[str]
    quiz: List[QuizQuestion]  # 5-10 questions
    related_topics: List[str]
```

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Issue 1: "Database connection error"

**Symptoms:**
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solutions:**
1. Verify PostgreSQL is running:
   ```bash
   # macOS/Linux
   sudo systemctl status postgresql
   
   # Windows
   Check Services app for PostgreSQL service
   ```

2. Check database credentials in `.env` file
3. Verify database exists:
   ```bash
   psql -U postgres -l
   ```

#### Issue 2: "GEMINI_API_KEY not found"

**Symptoms:**
```
ValueError: GEMINI_API_KEY not found in environment variables
```

**Solutions:**
1. Create `.env` file in `backend/` directory
2. Add your API key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```
3. Restart the backend server

#### Issue 3: "CORS error" in browser console

**Symptoms:**
```
Access to fetch at 'http://localhost:8000' has been blocked by CORS policy
```

**Solutions:**
1. Verify backend CORS settings in `main.py`:
   ```python
   allow_origins=["http://localhost:5173"]
   ```
2. Ensure frontend is running on port 5173
3. Restart both servers

#### Issue 4: Quiz generation takes too long or times out

**Symptoms:**
- Request hangs for over 2 minutes
- "Request timeout" error

**Solutions:**
1. Check your internet connection
2. Verify Gemini API key is valid
3. Try a shorter Wikipedia article
4. Check Gemini API rate limits
5. Review backend console for error messages

#### Issue 5: "Module not found" errors

**Symptoms:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solutions:**
1. Activate virtual environment:
   ```bash
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

#### Issue 6: Frontend not connecting to backend

**Symptoms:**
- "Network Error" in browser
- "Backend server is not responding"

**Solutions:**
1. Verify backend is running on port 8000
2. Check `API_BASE_URL` in `frontend/src/services/api.js`
3. Test backend directly:
   ```bash
   curl http://localhost:8000/health
   ```

---

## 🚀 Future Enhancements

### Planned Features

1. **User Authentication**
   - User accounts and login system
   - Personal quiz history per user
   - Quiz sharing capabilities

2. **Advanced Quiz Features**
   - True/False questions
   - Fill-in-the-blank questions
   - Image-based questions
   - Timed quiz mode
   - Leaderboards

3. **Enhanced Analytics**
   - Quiz performance tracking
   - Difficulty analysis
   - Topic mastery indicators
   - Study recommendations

4. **Export Capabilities**
   - Export quizzes to PDF
   - Print-friendly format
   - Share via link
   - Embed quizzes

5. **Multi-Language Support**
   - Support for non-English Wikipedia
   - Translation of quizzes
   - Localized UI

6. **Advanced Scraping**
   - Support for more sources (not just Wikipedia)
   - PDF and document upload
   - YouTube transcript processing

7. **Performance Optimizations**
   - Redis caching layer
   - Async processing with Celery
   - CDN integration
   - Database indexing

8. **Mobile Application**
   - React Native app
   - Offline quiz mode
   - Push notifications

---


---

## 👥 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 🙏 Acknowledgments

- **Google Gemini AI** for powering the quiz generation
- **Wikipedia** for providing free, open-access knowledge
- **FastAPI** for the excellent web framework
- **React** community for UI components and patterns
- **LangChain** for LLM integration abstractions

---

## 📧 Contact

For questions, issues, or suggestions:
- Create an issue on GitHub
- Email: kdhanunjay2704@gmail.com

---

## 🎓 Educational Use

This project is designed for educational purposes and demonstrates:
- Full-stack application development
- AI/LLM integration
- Web scraping techniques
- Database design and ORM usage
- RESTful API design
- Modern frontend development
- Prompt engineering best practices

Feel free to use this project as a learning resource or starting point for your own applications!

---

**Happy Learning! 🎓✨**