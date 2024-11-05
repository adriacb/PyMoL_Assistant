import os
import re
import json
import requests


import pymol
from pymol import cmd

from pymolassistant.logger import Logger

# Initialize the logger to the same directory as the server
logger2 = Logger(
    os.path.join(os.path.dirname(__file__), "logs/pymol-assistant-server-app.log"),
    )

def extend(funct: callable, name: str = None):
    if name is None:
        name = funct.__name__
    print(f"Function name: {name}")
    cmd.extend(name, funct)
    setattr(cmd, name, funct)

def get_current_selection() -> str:
    current_selection = cmd.get_object_list()
    # Format as a comma-separated string
    return ", ".join(current_selection) if current_selection else ""

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
        response = response.replace("```", "").replace("```", "").strip()
        
        # Attempt to load as JSON
        parsed_response = json.loads(response)
        
        print(f"Parsed response: {parsed_response}")
        return parsed_response
    
    except json.JSONDecodeError as e:
        logger2.error(f"Failed to parse response with JSON: {e}")
        return None


def question(input: str):
    # Send the question to the FastAPI server
    try:
        response = requests.post("http://127.0.0.1:8000/question", json={
            "question": input, 
            "current_slection": get_current_selection()          # We pass always the current loaded objects
            })
        logger2.info(f"Sending question: {input}")
        
        if response.status_code == 200:

            # Parse the response
            response = response.json()["final_response"]
            #print(response)
            if response:
                #logger2.info(f"Response: {response['usage']}, type: {type(response['usage'])}")
                print("PyMOL_Assistant>",response['answer'])
                print("PyMOL_Assistant>",response['references'])                
                try:
                    eval(response['usage'])
                except Exception as e:
                    print(f"Failed when using the response: {response['usage']}")
        else:
            print(f"Failed to send question. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error occurred: {e}")
    
    return {"question": input}

extend(question)

