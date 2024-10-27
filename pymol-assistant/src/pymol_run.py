import os
import re
import json
import requests


import pymol
from pymol import cmd

from src.logger import Logger

# Initialize the logger to the same directory as the server
logger2 = Logger(
    os.path.join(os.path.dirname(__file__), "logs/pymol-assistant-app.log"),
    )

def extend(funct, name:str=None):
    if name is None:
        name = funct.__name__
    print(f"Function name: {name}")
    cmd.extend(name, funct)
    setattr(cmd, name, funct)

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
        
        logger2.info(f"Parsed response: {parsed_response}")
        return parsed_response
    except json.JSONDecodeError as e:
        logger2.error(f"Failed to parse response with JSON: {e}")
        return None


def question(input: str):
    # Send the question to the FastAPI server
    try:
        response = requests.post("http://127.0.0.1:8000/question", json={"question": input})
        logger2.info(f"Sending question: {input}")
        
        if response.status_code == 200:
            logger2.info(f"Server response: {response.json()}")
            # Parse the response
            response = parse_response(response.json()["message"])
            print(response['usage'])

            if response:
                #logger2.info(f"Response: {response['usage']}, type: {type(response['usage'])}")
                
                try:
                    eval(response['usage'])
                except Exception as e:
                    logger2.error(f"Failed when using the response: {response['usage']}")
        else:
            logger2.error(f"Failed to send question. Status code: {response.status_code}")
    except Exception as e:
        logger2.critical(f"Error occurred: {e}")
    
    return {"question": input}

extend(question)

