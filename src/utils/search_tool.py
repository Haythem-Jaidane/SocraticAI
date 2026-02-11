from langchain_core.tools import Tool
from langchain_community.tools import DuckDuckGoSearchRun

# Initialize the search tool
search = DuckDuckGoSearchRun()

tools = [search]