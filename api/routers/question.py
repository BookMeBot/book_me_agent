from fastapi import APIRouter
from agents.question_agent import answer_question

router = APIRouter()


@router.post("/")
async def question_endpoint(context: str, question: str):
    answer = answer_question(context, question)
    return {"answer": answer}
