from langchain_classic.agents import create_tool_calling_agent,AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.memory import ConversationBufferWindowMemory
from ..utils.search_tool import tools
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_retries=6,
    timeout=60,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

memory = ConversationBufferWindowMemory(
    k=3, 
    memory_key="chat_history", 
    return_messages=True
)

prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are an AI Mentor and Tutor. Your goal is to foster deep understanding. "
     "When explaining: \n"
     "1. Start with a high-level concept.\n"
     "2. Provide clear technical details with step-by-step reasoning.\n"
     "3. Use analogies or examples where helpful.\n\n"
     "STRICT RULES:\n"
     "- NEVER rewrite or fix user code directly; instead, explain the logic so they can fix it themselves.\n"
     "- If using tools, synthesize the information into a teaching moment.\n"
     "- Maintain an encouraging, academic, yet accessible tone.\n\n"
     "FORMATTING:\n"
     "- Use Markdown for headers and bold text for key terms.\n"
     "- Always include a '### Resources' section at the very bottom with relevant hyperlinks for further reading."
    ),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])
# 3. Create the agent
# Note: Ensure your 'tools' list is defined before this point
agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    memory=memory, 
    verbose=True
)
