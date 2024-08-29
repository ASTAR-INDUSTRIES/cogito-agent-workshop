from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv

load_dotenv()

tool = TavilySearchResults(max_results=3)
tools = [tool]
