import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from src.logger import Logger
from src.models import QuestionModel
from src.prompts import *
from src.dag.workflow import graph


from langchain.schema import (
    HumanMessage,     # Humanessage is a message from the human
)

# TODO: config logger output directory in the config file
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

    input = {"messages": [
        HumanMessage(content=question.question)
        ]}
    config = {"configurable": {"thread_id": "thread-1"}} # Required for the graph to run with the memory saver
    output = graph.invoke(
        input=input,
        config=config
        )["messages"][-1].content
    
    return {"message": output}

@app.get("/graph")
def get_graph_image():
    # Path to the image file
    image_path = "dag/images/workflow.png"
    image_path = os.path.join(os.path.dirname(__file__), image_path)

    # Check if the file exists
    if not os.path.exists(image_path):
        logger.error(f"Image not found: {image_path}")
        raise HTTPException(status_code=404, detail="Image not found")

    # Serve the image
    return FileResponse(image_path, media_type="image/png")