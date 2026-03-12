from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

def build_dynamic_prompt(time_per_week, learning_need, deadline,format_instructions):
    return f"""
You are an AI mentor. You MUST output ONLY valid JSON.
No explanation, no markdown, no ```json blocks, no commentary.

Your task: create a structured SMART-goal weekly learning plan.

=== USER CONTEXT ===
Weekly available time: {time_per_week}
Learning goal: {learning_need}
Deadline: {deadline}

=== REQUIRED BEHAVIOR ===
- Break the plan logically by week
- Do NOT include success metrics or extra fields
- Missing information? Still output JSON matching schema
- Output *pure JSON only*

=== JSON FORMAT YOU MUST FOLLOW ===
{format_instructions}

Now answer using ONLY JSON.
"""

roadmap_prompt = ChatPromptTemplate.from_messages([
    ("system", build_dynamic_prompt("{time_per_week}", "{learning_need}", "{deadline}","{format_instructions}")),
    ("human", "{input}")
])