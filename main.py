import os

from dotenv import load_dotenv

load_dotenv()

import subprocess

# Load .env variables (API key, etc.)
load_dotenv()

# Ensure tracing is on
os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")


# Dynamically use the current Git branch (optional)
def current_branch():
    try:
        name = (
            subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"], stderr=subprocess.DEVNULL
            )
            .decode()
            .strip()
        )
        return name.replace("/", "-")
    except Exception:
        return "detached"


repo_name = "react-search-agent"
os.environ["LANGCHAIN_PROJECT"] = f"{repo_name}:{current_branch()}"

print(f"LangSmith project → {os.environ['LANGCHAIN_PROJECT']}")
# --- End LangSmith setup ---

from langchain import hub
from langchain.agents import AgentExecutor
from langchain.agents.react.agent import create_react_agent
##from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

# https://python.langchain.com/api_reference/langchain/agents/langchain.agents.react.agent.create_react_agent.html
# https://python.langchain.com/docs/how_to/agent_executor/


from prompt import REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS
from schemas import AgentResponse

tools = [TavilySearch()]
llm = ChatOpenAI(model="gpt-4")
structured_llm = llm.with_structured_output(AgentResponse)
#new llm that will use the structure the date according to AgentResponse
#because gpt-5 doens't support the stop function...
react_prompt = hub.pull("hwchase17/react")
# https://smith.langchain.com/hub/hwchase17/react?organizationId=7fb459f4-a2f4-4ff3-ae43-8b761403095f
## removed ## #output_parser = PydanticOutputParser(pydantic_object=AgentResponse)
react_prompt_with_format_instructions = PromptTemplate (
    template = REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS ,
    input_variables = ["input", "agent_scratchpad", "tool_names"]
).partial(format_instructions="")


agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=react_prompt_with_format_instructions
)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
extract_output = RunnableLambda (lambda x: x["output"])
#will turn everything to be "invokable"  x is the input => if x a disctionnnary, it will look for the "output" key and this is
#what will be return to us. So this is going to take the agent executors output.And it's going to extract the output key of it.
## removed ## parse_output = RunnableLambda(lambda x: output_parser.parse(x))
#will use the output_parser.parse function on the input it gets, where input = extract_output

chain = agent_executor | extract_output | structured_llm

def main():
    result = chain.invoke(
        input={
            "input": "search for 3 job postings for an ai engineer using langchain in the bay area on linkedin and list their details",
        }
    )
    print(result)


if __name__ == "__main__":
    main()
