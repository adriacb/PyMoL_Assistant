import os
import requests

import pymol
from pymol import cmd

from src.logger import Logger

# Initialize the logger to the same directory as the server
logger = Logger(os.path.join(os.path.dirname(__file__), "logs/pymol-assistant-app.log"))

def extend(funct, name:str=None):
    if name is None:
        name = funct.__name__
    print(f"Function name: {name}")
    cmd.extend(name, funct)
    setattr(cmd, name, funct)

def literal_eval(input: str):
    # Evaluate the input as a Python literal
    try:
        result = eval(input)
        logger.info(f"Evaluated input: {result}")
    except Exception as e:
        logger.error(f"Failed to evaluate input: {e}")
        result = None

def question(input: str):
    # Send the question to the FastAPI server
    try:
        response = requests.post("http://127.0.0.1:8000/question", json={"question": input})
        logger.info(f"Sending question: {input}")
        
        if response.status_code == 200:
            logger.info(f"Server response: {response.json()}")
            if "action" in response.json():
                literal_eval(response.json().get("action"))
        else:
            logger.error(f"Failed to send question. Status code: {response.status_code}")
    except Exception as e:
        logger.critical(f"Error occurred: {e}")
    
    return {"question": input}

extend(question)

