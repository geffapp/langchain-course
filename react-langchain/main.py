from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool  # stable import path
from langchain_core.tools import render_text_description
from langchain_openai import ChatOpenAI
from langchain.agents.output_parsers import ReActSingleInputOutputParser

load_dotenv ()

##1 usage
@tool ##get the function and create a langchain tool out of it 
def get_text_length(text: str) -> int:
    """Returns the length of the given text by characters."""  ###important as it will help the LLM
    
    print (f"get_text_length enter with {text=}")
    text = text.strip ("'\n").strip('"')
    ##stripping aways non-alphabetic characters that may have been added by the LLM
   
    return len(text)

if __name__ == "__main__":
    print("Hello ReAct Langchain!")
    tools = [get_text_length]

    template= """
    Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!
  
    Question: {input}
    Thought:
    """

    prompt = PromptTemplate.from_template (template = template).partial (
        tools = render_text_description(tools), tool_names = ", ".join ([t.name for t in tools])
        )
    
    llm = ChatOpenAI (temperature = 0, stop=["\nObservation:"])
    ## the way to use observation, depends on the model (parse error in this case)
    agent = {"input": lambda x:x ["input"]} | prompt | llm | ReActSingleInputOutputParser ()

    res = agent.invoke({"input": "What is the length of the text 'DOG'?|in characters"})
    print (res)