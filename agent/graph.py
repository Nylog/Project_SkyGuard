"""
Builds the SkyGuard agent using LangGraph.
The agent is powered by a local Qwen2.5 model (via Ollama) and has access
to the flight_status_tool, which combines flight data and weather
conditions for a given flight number.
"""

from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
# Note: deprecated as of LangGraph v1 in favor of langchain.agents.create_agent,but still works correctly. 
# Keeping this version since it's already tested and working.
# If this stops working in the future, switch to:
# from langchain.agents import create_agent

from agent.tools import get_flight_status, report_lost_baggage, check_baggage_status

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

SYSTEM_PROMPT = """
You are Skyguard, the operational assistant for Celestial Line.
You help staff and passengers with flight status, maintenance-related and general service request.
Be concise, factual and professional.

When looking up a flight, always use the exact flight number the user provided, never a different or made-up one.
If the user's message does not include a flight number and one is needed to answer, ask them to provide it instead of guessing.
If you don't have information about something, say so clearly instead of guessing.
"""


@tool # Converts the function into a LangChain tool the agent can use when needed

def flight_status_tool(flight_number : str) -> dict:
    """Get the current status, route, and weather conditions for a given flight number."""
    result = get_flight_status(flight_number)
    if result is None:
        return {"error" : f"No flight found with number: {flight_number}"}
    return result


@tool
def report_lost_baggage_tool(flight_number : str, description : str) -> dict:
    """ Reports a lost baggage for a given flight, with a description of the item. Returns a reference number.""".

    return report_lost_baggage(flight_number, description)


@tool
def check_baggage_status_tool(reference_number : str) -> dict:
    """ hecks the status of a previously reported lost baggage, given its reference number."""
    return check_baggage_status(reference_number)


llm = ChatOllama(model = "qwen2.5:7b-instruct", temperature = 0)

agent = create_react_agent(llm, tools = [flight_status_tool], prompt = SYSTEM_PROMPT)
# If this stops working in the future, switch to:
# agent = create_agent(llm, tools = [flight_status_tool], system_prompt = SYSTEM_PROMPT)
