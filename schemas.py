from typing import List

from pydantic import BaseModel, Field
# core pydantic class we will inheritate from to create our own base model and data objects. 
# And when we create the class that is going to inherit from base model, we get automatic validations,
# realization from JSON and ID auto complete. field is a function that lets us add extra validation 
# and metadata to our model attributes (contraints like min/ max...)

class Source (BaseModel):
    """schema for a source used by the agent"""

    url : str = Field (description = "The URL of the source")

class AgentResponse (BaseModel):
    """Schema for agent response with answer and sources"""

    answer: str = Field (description = "the agent's answer to the query")
    sources: List [Source] = Field (
        default_factory=list, description="List of Sources used to generate the answer"
    )

    