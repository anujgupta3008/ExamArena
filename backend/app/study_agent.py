from typing import Dict, Any, List
from google.antigravity import Agent, LocalAgentConfig
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Exam, Topic, Question, User, UserResponse

def get_topic_stats(exam_id: int, topic_name: str) -> str:
    """Fetches historical statistics for a topic in an exam.
    
    Args:
        exam_id: The ID of the exam.
        topic_name: The name of the topic.
    """
    db = SessionLocal()
    try:
        topic = db.query(Topic).filter(Topic.name.ilike(f"%{topic_name}%")).first()
        if not topic:
            return f"Topic '{topic_name}' not found."
            
        questions = db.query(Question).filter(
            (Question.topic_id == topic.id) | (Question.secondary_topic_id == topic.id)
        ).all()
        
        count = len(questions)
        marks = sum([q.marks for q in questions if q.marks])
        return f"Topic '{topic.name}' has {count} questions totaling {marks} marks historically."
    finally:
        db.close()

def get_predictions(exam_id: int) -> str:
    """Fetches AI predictions of important topics for the next exam.
    
    Args:
        exam_id: The ID of the exam.
    """
    db = SessionLocal()
    try:
        exam = db.query(Exam).filter(Exam.id == exam_id).first()
        if not exam or not exam.predicted_topics:
            return "No predictions available for this exam yet."
        return f"Predictions for {exam.name}: {exam.predicted_topics}"
    finally:
        db.close()

def get_user_performance(user_id: int) -> str:
    """Fetches the user's weakness areas based on their past quiz performance.
    
    Args:
        user_id: The ID of the user.
    """
    db = SessionLocal()
    try:
        responses = db.query(UserResponse).filter(UserResponse.user_id == user_id, UserResponse.is_correct == False).all()
        if not responses:
            return "User has no incorrect answers yet. They are doing great!"
        
        weaknesses = {}
        for r in responses:
            topic_name = r.question.topic.name if r.question and r.question.topic else "General"
            weaknesses[topic_name] = weaknesses.get(topic_name, 0) + 1
            
        sorted_weaknesses = sorted(weaknesses.items(), key=lambda x: x[1], reverse=True)
        weak_str = ", ".join([f"{t} ({c} mistakes)" for t, c in sorted_weaknesses[:5]])
        return f"User's top weaknesses: {weak_str}"
    finally:
        db.close()

def generate_study_plan(exam_id: int, days: int, weaknesses: str) -> str:
    """Creates a personalized study plan based on weaknesses.
    
    Args:
        exam_id: The ID of the exam.
        days: Number of days until the exam.
        weaknesses: The user's top weaknesses.
    """
    return f"Suggested {days}-day plan: Focus 60% on resolving these weaknesses: {weaknesses}. Spend 40% on past paper revisions."

agent_tools = [
    get_topic_stats,
    get_predictions,
    get_user_performance,
    generate_study_plan
]

async def chat_with_advisor(message: str, user_id: int, exam_id: int) -> str:
    config = LocalAgentConfig(
        tools=agent_tools,
        system_instructions=(
            f"You are an AI Study Advisor for an exam preparation platform. "
            f"The user ID is {user_id} and exam ID is {exam_id}. "
            "Use the provided tools to fetch stats, AI predictions, and user weaknesses, "
            "then give tailored advice and generate study plans. "
            "Format your responses in clear Markdown."
        )
    )
    
    async with Agent(config) as agent:
        response = await agent.chat(message)
        full_response = ""
        async for chunk in response:
            full_response += chunk
        return full_response
