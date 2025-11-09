# llm_quiz_generator.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import json
import re

# Load environment variables
load_dotenv()


def get_llm():
    """Initialize and return the Gemini LLM"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-latest",
        google_api_key=api_key,
        temperature=0.3,  # Lower temperature for more consistent output
        convert_system_message_to_human=True
    )
    return llm


def extract_json_from_response(text: str) -> str:
    """
    Robustly extract JSON from LLM response.
    Handles multiple formats and edge cases.
    """
    # Remove markdown code blocks
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    text = text.strip()
    
    # Method 1: Find balanced braces
    brace_count = 0
    start_idx = -1
    
    for i, char in enumerate(text):
        if char == '{':
            if brace_count == 0:
                start_idx = i
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0 and start_idx != -1:
                json_str = text[start_idx:i+1]
                # Validate it's proper JSON
                try:
                    json.loads(json_str)
                    return json_str
                except:
                    continue
    
    # Method 2: Use regex to find JSON-like structure
    json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    matches = re.finditer(json_pattern, text, re.DOTALL)
    
    for match in matches:
        try:
            json_str = match.group(0)
            json.loads(json_str)
            return json_str
        except:
            continue
    
    # Method 3: Try the whole text
    try:
        json.loads(text)
        return text
    except:
        pass
    
    raise ValueError("Could not extract valid JSON from response")


def create_strict_prompt():
    """Create a very strict prompt that enforces single JSON output"""
    
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

    return ChatPromptTemplate.from_template(template)


def validate_and_fix_quiz_data(data: dict, title: str) -> dict:
    """
    Validate and auto-fix common issues in quiz data.
    Returns a valid quiz data structure.
    """
    fixed_data = {}
    
    # Fix summary
    fixed_data['summary'] = data.get('summary', f"An educational article about {title}")[:500]
    
    # Fix key_entities
    entities = data.get('key_entities', {})
    if not isinstance(entities, dict):
        entities = {}
    
    fixed_data['key_entities'] = {
        'people': entities.get('people', [])[:10] if isinstance(entities.get('people'), list) else [],
        'organizations': entities.get('organizations', [])[:10] if isinstance(entities.get('organizations'), list) else [],
        'locations': entities.get('locations', [])[:10] if isinstance(entities.get('locations'), list) else []
    }
    
    # Fix sections
    sections = data.get('sections', [])
    if not isinstance(sections, list):
        sections = []
    fixed_data['sections'] = sections[:15]
    
    # Fix quiz questions
    quiz = data.get('quiz', [])
    if not isinstance(quiz, list):
        quiz = []
    
    fixed_questions = []
    for q in quiz:
        if not isinstance(q, dict):
            continue
        
        # Validate question structure
        question_text = q.get('question', '').strip()
        options = q.get('options', [])
        answer = q.get('answer', '').strip()
        difficulty = q.get('difficulty', 'medium').lower()
        explanation = q.get('explanation', '').strip()
        
        # Skip invalid questions
        if not question_text or not options or not answer:
            continue
        
        # Ensure exactly 4 options
        if not isinstance(options, list):
            continue
        
        if len(options) < 4:
            continue
        
        if len(options) > 4:
            options = options[:4]
        
        # Ensure answer is in options
        if answer not in options:
            answer = options[0]
        
        # Ensure valid difficulty
        if difficulty not in ['easy', 'medium', 'hard']:
            difficulty = 'medium'
        
        # Ensure explanation exists
        if not explanation:
            explanation = f"The correct answer is {answer}."
        
        fixed_questions.append({
            'question': question_text,
            'options': options,
            'answer': answer,
            'difficulty': difficulty,
            'explanation': explanation
        })
        
        # Stop at 10 questions max
        if len(fixed_questions) >= 10:
            break
    
    fixed_data['quiz'] = fixed_questions
    
    # Fix related_topics
    topics = data.get('related_topics', [])
    if not isinstance(topics, list):
        topics = []
    fixed_data['related_topics'] = topics[:10]
    
    return fixed_data


def generate_quiz(title: str, content: str, max_retries: int = 3) -> dict:
    """
    Generate a quiz from Wikipedia article content with retry logic.
    
    Args:
        title: Article title
        content: Cleaned article content
        max_retries: Number of retry attempts if generation fails
        
    Returns:
        Dictionary containing the generated quiz data
    """
    
    # Truncate content to fit token limits
    max_content_length = 20000  # Conservative limit
    if len(content) > max_content_length:
        print(f"⚠️ Content truncated from {len(content)} to {max_content_length} characters")
        content = content[:max_content_length]
    
    llm = get_llm()
    prompt = create_strict_prompt()
    
    for attempt in range(max_retries):
        try:
            print(f"\n{'='*80}")
            print(f"🤖 Quiz Generation Attempt {attempt + 1}/{max_retries}")
            print(f"📝 Article: {title}")
            print(f"📄 Content length: {len(content)} characters")
            print(f"{'='*80}")
            
            # Format and invoke
            formatted_prompt = prompt.format(title=title, content=content)
            
            print("🔄 Calling Gemini API...")
            response = llm.invoke(formatted_prompt)
            
            # Extract response text
            response_text = response.content if hasattr(response, 'content') else str(response)
            print(f"📥 Received response ({len(response_text)} characters)")
            
            # Extract JSON
            print("🔍 Extracting JSON from response...")
            json_text = extract_json_from_response(response_text)
            print(f"✂️ Extracted JSON ({len(json_text)} characters)")
            
            # Parse JSON
            print("📊 Parsing JSON...")
            raw_data = json.loads(json_text)
            
            # Validate and fix
            print("🔧 Validating and fixing data structure...")
            fixed_data = validate_and_fix_quiz_data(raw_data, title)
            
            # Final validation
            if len(fixed_data['quiz']) < 5:
                raise ValueError(f"Only generated {len(fixed_data['quiz'])} questions, need at least 5")
            
            print(f"\n{'='*80}")
            print("✅ Quiz Generated Successfully!")
            print(f"{'='*80}")
            print(f"📊 Summary length: {len(fixed_data['summary'])} characters")
            print(f"👥 Key entities:")
            print(f"   - People: {len(fixed_data['key_entities']['people'])}")
            print(f"   - Organizations: {len(fixed_data['key_entities']['organizations'])}")
            print(f"   - Locations: {len(fixed_data['key_entities']['locations'])}")
            print(f"📑 Sections: {len(fixed_data['sections'])}")
            print(f"❓ Questions: {len(fixed_data['quiz'])}")
            print(f"🔗 Related topics: {len(fixed_data['related_topics'])}")
            
            # Show difficulty distribution
            difficulty_count = {'easy': 0, 'medium': 0, 'hard': 0}
            for q in fixed_data['quiz']:
                difficulty_count[q['difficulty']] += 1
            print(f"📈 Difficulty: Easy={difficulty_count['easy']}, Medium={difficulty_count['medium']}, Hard={difficulty_count['hard']}")
            print(f"{'='*80}\n")
            
            return {
                "success": True,
                "data": fixed_data,
                "error": None
            }
            
        except Exception as e:
            error_msg = str(e)
            print(f"\n❌ Attempt {attempt + 1} failed: {error_msg}")
            
            if attempt < max_retries - 1:
                print(f"🔄 Retrying... ({max_retries - attempt - 1} attempts remaining)")
                # Reduce content size for retry
                content = content[:len(content)//2]
                print(f"📉 Reduced content to {len(content)} characters for retry")
            else:
                print(f"\n{'='*80}")
                print("❌ All retry attempts exhausted")
                print(f"{'='*80}")
                import traceback
                traceback.print_exc()
                return {
                    "success": False,
                    "data": None,
                    "error": f"Failed after {max_retries} attempts: {error_msg}"
                }
    
    return {
        "success": False,
        "data": None,
        "error": "Quiz generation failed"
    }


def validate_quiz_output(quiz_data: dict) -> tuple:
    """
    Final validation of quiz output.
    
    Args:
        quiz_data: Generated quiz dictionary
        
    Returns:
        Tuple of (is_valid: bool, error_message: str)
    """
    try:
        # Check required fields
        required_fields = ['summary', 'key_entities', 'sections', 'quiz', 'related_topics']
        for field in required_fields:
            if field not in quiz_data:
                return False, f"Missing required field: {field}"
        
        # Check quiz has minimum questions
        if len(quiz_data['quiz']) < 5:
            return False, f"Quiz has only {len(quiz_data['quiz'])} questions, need at least 5"
        
        # Check each question structure
        for i, q in enumerate(quiz_data['quiz'], 1):
            if 'question' not in q or not q['question']:
                return False, f"Question {i} missing question text"
            
            if 'options' not in q or len(q['options']) != 4:
                return False, f"Question {i} must have exactly 4 options"
            
            if 'answer' not in q or q['answer'] not in q['options']:
                return False, f"Question {i} answer must be one of the options"
            
            if 'difficulty' not in q or q['difficulty'] not in ['easy', 'medium', 'hard']:
                return False, f"Question {i} has invalid difficulty"
            
            if 'explanation' not in q or not q['explanation']:
                return False, f"Question {i} missing explanation"
        
        return True, None
        
    except Exception as e:
        return False, f"Validation error: {str(e)}"