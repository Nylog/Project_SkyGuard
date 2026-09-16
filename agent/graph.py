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

from agent.tools import get_flight_status, report_lost_baggage, check_baggage_status, calculate_fuel_load, get_seat_amenities

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))



SYSTEM_PROMPT = """
You are Skyguard, the operational assistant for Celestial Line.
You help staff and passengers with flight status, maintenance-related and general service request.
Be concise, factual and professional.

You only answer questions related to Celestial Line's flights, baggage, maintenance, and passenger services.
If asked about anything unrelated to these topics (general knowledge, entertainment, sport, or any other subject), 
politely explain that you can only help with flight-related operations and cannot answer that question.

When looking up a flight, always use the exact flight number the user provided, never a different or made-up one.
If the user's message does not include a flight number and one is needed to answer, ask them to provide it instead of guessing.
If a passenger reports lost baggage, ask for the flight number and a brief description if not already provided, then use the reporting tool.
If a passenger asks about seat amenities, ask for the flight number and seat number if not already provided.
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
    """ Reports a lost baggage for a given flight, with a description of the item. Returns a reference number."""
    return report_lost_baggage(flight_number, description)


@tool
def check_baggage_status_tool(reference_number : str) -> dict:
    """ hecks the status of a previously reported lost baggage, given its reference number."""
    return check_baggage_status(reference_number)


@tool
def calculate_fuel_load_tool(flight_number : str, passengers : int) -> dict:
    """Calculates the estimated fuel load (in liters) for a flight, given the number of passengers. Admin only."""
    return calculate_fuel_load(flight_number, passengers)


@tool
def seat_amenities_tool(flight_number : str, seat_number :  str) -> dict:
    """Checks seat details (window/aisle/middle, USB, power outlet, TV) for a given flight and seat number."""
    return get_seat_amenities(flight_number, seat_number)



llm = ChatOllama(model = "qwen2.5:7b-instruct", temperature = 0)

BASE_TOOLS = [flight_status_tool, report_lost_baggage_tool, check_baggage_status_tool, seat_amenities_tool]
ADMIN_TOOLS = [calculate_fuel_load_tool]

def build_agent(role):
    """
    Builds an agent with the tool set appropriate for the given role.
    Admin-only tools (like fuel calculation) are only included when role == "admin",
    so the LLM cannot call them at all for other roles
    """
     
    tools = BASE_TOOLS.copy()

    if role == "admin":
        tools += ADMIN_TOOLS

    return create_react_agent(llm, tools = tools, prompt = SYSTEM_PROMPT )
# If this stops working in the future, switch to:
# agent = create_agent(llm, tools = [flight_status_tool], system_prompt = SYSTEM_PROMPT)


