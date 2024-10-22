import argparse
from fastapi import FastAPI, Request
from pydantic import BaseModel

# FastAPI app instance
app = FastAPI()

class QuestionModel(BaseModel):
    question: str

@app.post("/question")
async def submit_question(question: QuestionModel):
    # Process the received question
    print(f"Received question: {question.question}")
    return {"message": f"Received question: {question.question}"}