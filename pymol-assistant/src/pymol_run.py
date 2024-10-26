import os
import re
import json
import requests


import pymol
from pymol import cmd

from src.logger import Logger

# Initialize the logger to the same directory as the server
logger = Logger(
    os.path.join(os.path.dirname(__file__), "logs/pymol-assistant-app.log")
    )

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

def parse_response(response: str) -> dict:
    """
    Parse the response from the user.

    Args:
        response (str): The response from the user.

    Returns:
        dict: The parsed response.
    """
    try:
        # Remove code markers
        response = response.replace("```json", "").replace("```", "").strip()
        
        # Attempt to load as JSON
        parsed_response = json.loads(response)
        
        logger.info(f"Parsed response: {parsed_response}")
        return parsed_response
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse response with JSON: {e}")
        return None


def question(input: str):
    # Send the question to the FastAPI server
    try:
        response = requests.post("http://127.0.0.1:8000/question", json={"question": input})
        logger.info(f"Sending question: {input}")
        
        if response.status_code == 200:
            logger.info(f"Server response: {response.json()}")
            
            # Parse the response
            response = parse_response(response.json()["message"])
            
            if response:
                logger.info(f"Response: {response['usage']}, type: {type(response['usage'])}")
                literal_eval(response['usage'])
        else:
            logger.error(f"Failed to send question. Status code: {response.status_code}")
    except Exception as e:
        logger.critical(f"Error occurred: {e}")
    
    return {"question": input}

extend(question)

