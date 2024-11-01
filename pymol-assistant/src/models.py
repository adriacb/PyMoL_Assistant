from typing import Type
from pydantic import BaseModel, Field

class QuestionModel(BaseModel):
    question: str

class FinalResponse(BaseModel):
    """Final response to the user."""
    answer: str = Field(description="A friendly answer to the user's query.")
    usage: str = Field(
        description="cmd.function_name(parameters) - The usage of the function (it always starts with 'cmd.') and parameters (if any).",
        default=""
        )
    references: str = Field(
        description="A link reference to the PyMoL documentation or any other source that supports your answer (if any).",
        default=""
        )

class RagSearchSchema(BaseModel):
    query: str = Field(description="The query to search the PyMOL documentation.")
    top_k: int = Field(description="The number of results to return.", default=4)