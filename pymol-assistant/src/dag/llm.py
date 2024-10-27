from langchain_openai import ChatOpenAI
from src.dag.tools import tools

# OpenAI chat instance
model = ChatOpenAI(
    model='gpt-4o-mini',
    temperature=0.5,
).bind_tools(tools)