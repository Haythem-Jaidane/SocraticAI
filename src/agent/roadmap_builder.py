from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from ..core.llm import llm
from ..prompts.roadmap import roadmap_prompt


# ---------------------------
# 1️⃣ Input Schema
# ---------------------------

class ContactInfo(BaseModel):
    time: int = Field(description="Available hours per week")
    need: str = Field(description="What to learn")
    deadline: str = Field(description="Learning deadline")
    question: str = Field(description="User question")


from typing import List

# ---------------------------
# 2️⃣ Output Schema
# ---------------------------

class WeeklyPlan(BaseModel):
    week: int = Field(description="The sequential number of the week")
    goal: str = Field(description="The primary learning objective for this week")
    # FUTURE TODO: Extend with fields like resources, estimated_hours, etc.

class LearningPlanResponse(BaseModel):
    plan: List[WeeklyPlan] = Field(description="The complete structured learning sequence")

parser = JsonOutputParser(pydantic_object=LearningPlanResponse)


# ---------------------------
# 3️⃣ Main Function
# ---------------------------

def generate_learning_plan(contact: ContactInfo):

    format_instructions = parser.get_format_instructions()

    chain = roadmap_prompt | llm | parser

    response = chain.invoke({
        "time_per_week":contact.time,
        "learning_need":contact.need,
        "deadline":contact.deadline,
        "format_instructions":format_instructions,
        "input":contact.question
    })

    return response
