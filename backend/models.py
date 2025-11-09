# models.py
from pydantic import BaseModel, Field
from typing import List, Dict

class QuizQuestion(BaseModel):
    """Schema for a single quiz question"""
    question: str = Field(description="The quiz question text")
    options: List[str] = Field(description="Four answer options (A, B, C, D)")
    answer: str = Field(description="The correct answer (must be one of the options)")
    difficulty: str = Field(description="Difficulty level: easy, medium, or hard")
    explanation: str = Field(description="Brief explanation of why this is the correct answer")


class KeyEntities(BaseModel):
    """Schema for extracted key entities"""
    people: List[str] = Field(default=[], description="Important people mentioned in the article")
    organizations: List[str] = Field(default=[], description="Organizations mentioned in the article")
    locations: List[str] = Field(default=[], description="Locations mentioned in the article")


class QuizOutput(BaseModel):
    """Complete schema for quiz generation output"""
    summary: str = Field(description="Brief 2-3 sentence summary of the article")
    key_entities: KeyEntities = Field(description="Key entities extracted from the article")
    sections: List[str] = Field(description="Main section titles from the article")
    quiz: List[QuizQuestion] = Field(description="List of 5-10 quiz questions")
    related_topics: List[str] = Field(description="3-5 related Wikipedia topics for further reading")


# Response models for FastAPI
class QuizGenerateRequest(BaseModel):
    """Request model for quiz generation endpoint"""
    url: str = Field(description="Wikipedia article URL")


class QuizGenerateResponse(BaseModel):
    """Response model for quiz generation endpoint"""
    id: int
    url: str
    title: str
    date_generated: str
    summary: str
    key_entities: Dict
    sections: List[str]
    quiz: List[Dict]
    related_topics: List[str]


class QuizHistoryItem(BaseModel):
    """Response model for quiz history items"""
    id: int
    url: str
    title: str
    date_generated: str


class ErrorResponse(BaseModel):
    """Response model for errors"""
    error: str
    details: str = None