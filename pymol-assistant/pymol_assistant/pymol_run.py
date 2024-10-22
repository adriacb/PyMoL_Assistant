import requests

import pymol
from pymol import cmd

from pymol_assistant.logger import Logger

# Initialize the logger
logger = Logger("logs/pymol-assistant.log")

def extend(funct, name:str=None):
    if name is None:
        name = funct.__name__
    print(f"Function name: {name}")
    cmd.extend(name, funct)
    setattr(cmd, name, funct)

def question(input: str):
    # Send the question to the FastAPI server
    try:
        response = requests.post("http://127.0.0.1:8000/question", json={"question": input})
        logger.info(f"Sending question: {input}")
        if response.status_code == 200:
            logger.info(f"Server response: {response.json()}")
        else:
            logger.error(f"Failed to send question. Status code: {response.status_code}")
    except Exception as e:
        logger.critical(f"Error occurred: {e}")
    
    return {"question": input}


extend(question)

