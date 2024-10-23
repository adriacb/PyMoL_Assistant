import os
from fastapi import FastAPI
from src.logger import Logger
from src.models import QuestionModel

logger = Logger(os.path.join(os.path.dirname(__file__), "logs/pymol-assistant-server.log"))
# FastAPI app instance
app = FastAPI()


@app.post("/question")
async def submit_question(question: QuestionModel) -> dict:
    """
    Asyncronously, get the question from the client and return the response.

    Args:
        question (QuestionModel): The question from the client.
    
    Returns:
        json: The response to the question.
    """
        # Process the received question
    logger.info(f"Received question: {question.question}")
    if question.question == "Get the structure 1a8o":
        return {"action": "cmd.fetch('1a8o')"}
    elif question.question == "show surface":
        return {"action": "cmd.show('surface')"}
    # Return the received question
    else:
        return {"message": f"Received question: {question.question}"}
    
    # question("Get the structure 1a8o")


@app.post("/question")
async def submit_question2(question: QuestionModel) -> dict:
    """
    Asyncronously, get the question from the client and return the response.

    Args:
        question (QuestionModel): The question from the client.
    
    Returns:
        json: The response to the question.
    """
        # Process the received question
    logger.info(f"Received question: {question.question}")
    
    # The question is transformed to HumanMessage
    #prompt = HumanMessage(content=question.question)

    # The 
    