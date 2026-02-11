from langchain_classic.agents import create_tool_calling_agent,AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.memory import ConversationBufferWindowMemory
from ..utils.search_tool import tools
from ..core.llm import llm

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
     "4. Provide used libery and modules\n"
     "5. Use exemple of code.\n\n"
     "STRICT RULES:\n"
     "- NEVER rewrite or fix user code directly; instead, explain the logic so they can fix it themselves.\n"
     "- If using tools, synthesize the information into a teaching moment.\n"
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
