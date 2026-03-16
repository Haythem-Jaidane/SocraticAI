from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from typing import List, TypedDict, Any, Optional

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

class LearningPlanResponse(BaseModel):
    plan: List[WeeklyPlan] = Field(description="The complete structured learning sequence")

class UserInfo(TypedDict):
    skills: str
    goal: str
    occupation: str

parser = JsonOutputParser(pydantic_object=LearningPlanResponse)


# ---------------------------
# 3️⃣ Main Function
# ---------------------------

def generate_learning_plan(contact: ContactInfo, *args, **kwargs):
    user_info = kwargs.get("user_info")
    if not user_info and args:
        user_info = args[0]
    
    print(f"DEBUG: generate_learning_plan called with kwargs keys: {list(kwargs.keys())}")

    format_instructions = parser.get_format_instructions()

    chain = roadmap_prompt | llm | parser

    user_context = ""
    if user_info:
        skills = user_info.get("skills", "Not specified")
        occupation = user_info.get("occupation", "Not specified")
        goal = user_info.get("goal", "Not specified")
        user_context = f"""
=== USER BACKGROUND ===
- Occupation: {occupation}
- Existing Skills: {skills}
- Long-term Goal: {goal}
"""

    response = chain.invoke({
        "time_per_week": contact.time,
        "learning_need": contact.need,
        "deadline": contact.deadline,
        "format_instructions": format_instructions,
        "input": contact.question,
        "user_context": user_context
    })

    return response
