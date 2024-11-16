from fastapi import APIRouter
from agents.qa_agent import answer_question

router = APIRouter()

@router.post("/")
async def qa_endpoint(context: str, question: str):
    answer = answer_question(context, question)
    return {"answer": answer}
