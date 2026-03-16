from pydantic import BaseModel, Field
from typing import List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from ..core.llm import llm

# ---------------------------
# 1️⃣ Output Schema
# ---------------------------

class Option(BaseModel):
    label: str = Field(description="A, B, C, or D")
    text: str = Field(description="The text of the option")

class Question(BaseModel):
    question: str = Field(description="The quiz question")
    options: List[Option] = Field(description="Exactly 4 options")
    correct_answer: str = Field(description="The label of the correct option (A, B, C, or D)")
    explanation: str = Field(description="Detailed explanation of why the answer is correct")

class QuizResponse(BaseModel):
    topic: str = Field(description="The topic of the quiz")
    questions: List[Question] = Field(description="List of questions")

parser = JsonOutputParser(pydantic_object=QuizResponse)

# ---------------------------
# 2️⃣ Prompt Template
# ---------------------------

quiz_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert educator. Generate a challenging quiz on the given topic. "
               "Ensure questions are varied and cover different aspects of the subject. "
               "Format the output as JSON according to these instructions: {format_instructions}"),
    ("human", "Generate a quiz with {num_questions} questions on the topic: {topic}")
])

# ---------------------------
# 3️⃣ Main Function
# ---------------------------

def generate_quiz(topic: str, num_questions: int = 5):
    """
    Generates a structured JSON quiz using the LLM.
    """
    chain = quiz_prompt | llm | parser
    
    response = chain.invoke({
        "topic": topic,
        "num_questions": num_questions,
        "format_instructions": parser.get_format_instructions()
    })
    
    return response
