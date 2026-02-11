from langchain_community.tools import ArxivQueryRun

arxiv = ArxivQueryRun()

tools = [arxiv]