import os
import uuid

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from src.logger import Logger
from src.models import QuestionModel
from src.prompts import *
from src.dag.workflow import graph

from langchain.schema import HumanMessage
from langchain_core.runnables import RunnableConfig

# TODO: config logger output directory in the config file
logger = Logger(os.path.join(os.path.dirname(__file__), "logs/pymol-assistant-server.log"))
# FastAPI app instance
app = FastAPI()

session_id = str(uuid.uuid4())

########### Routes ###########
@app.post("/question")
async def submit_question(question: QuestionModel, session_id: str = session_id):
    """
    Asyncronously, get the question from the client and return the response.

    Args:
        question (QuestionModel): The question from the client.
    
    Returns:
        json: The response to the question.
    """

    # Create a new session id if not provided
    config = RunnableConfig(configurable={
        "thread_id": "Thread-1",
        "session_id": session_id,
        "recursion_limit": 10,
        "llm": "gpt-4o-mini"
        })
    
    if "configurable" not in config or "thread_id" not in config["configurable"]:
        raise ValueError(
            "Make sure that the config includes the following information: {'configurable': {'thread_id': 'some_value'}}"
        )
    message = f"Question: {question.question}, current loaded objects : {question.current_slection}"
    logger.info(message)
    
    # the input to the graph is the chat history and the new question
    input = {
        "count": 0,
        "messages": [HumanMessage(content=message)]
        }

    # Required for the graph to run with the memory saver
    output = await graph.ainvoke(
        input=input,
        config=config,
        debug=True
        )

    content = output["messages"][-2].content[0]['input']
    print(content)
    return {"final_response": content}

    # For OpenAI
    # # Whether it comes directly form the Agent:
    # if output["messages"][-2].content:
    #     return {"final_response": output["messages"][-2].content}
    # else:

    #     return {
    #         "final_response": 
    #         output["messages"][-2].additional_kwargs["tool_calls"][0]["function"]["arguments"]
    #             }


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