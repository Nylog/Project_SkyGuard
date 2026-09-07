from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from tools import get_flight_status

SYSTEM_PROMPT = """
You are Skyguard, the operational assistent fot Celestial Line.
You help staff and passenger with flight status, mainteance-related and general service request.
Be concise, factual and professional.
If you don't have information about something, say so clearly instead og guessing.
"""


@tool # Converts the function into a LangChain tool the agent can use when needed

def flight_status_tool(flight_number : str) -> dict:
    """Get the current status, route, and weather conditions for a given flight number."""
    result = get_flight_status(flight_number)
    if result is None:
        return {"error" : f"No flight found with number: {flight_number}"}
    return result

