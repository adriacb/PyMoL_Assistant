from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from src.dag.tools import tools


# # OpenAI chat instance
# model = ChatOpenAI(
#     model='gpt-4o-mini',
#     temperature=0.5,
# ).bind_tools(
#     tools=tools,
#     tool_choice='any', 
#     strict=False
#     )

model = ChatAnthropic(
    model="claude-3-sonnet-20240229",
    temperature=0.5,
              ).bind_tools(
    tools=tools,
    tool_choice='any'
    )