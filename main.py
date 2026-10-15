
import os
import certifi
import requests

from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

os.environ["SSL_CERT_FILE"] = certifi.where()

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env")

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY is missing from .env")

if not WEATHERSTACK_API_KEY:
    raise ValueError("WEATHERSTACK_API_KEY is missing from .env")


# ==========================================
# TOOL 1: INTERNET SEARCH
# ==========================================

search_tool = TavilySearch(
    max_results=2
)


# ==========================================
# TOOL 2: CURRENT WEATHER
# ==========================================

@tool
def get_weather_data(city: str) -> str:
    """Get the current weather for a city using Weatherstack."""

    url = "https://api.weatherstack.com/current"

    params = {
        "access_key": WEATHERSTACK_API_KEY,
        "query": city
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        if "current" not in data:
            error = data.get("error", "Unknown API error")
            return f"Could not fetch weather for {city}: {error}"

        current = data["current"]

        temperature = current.get("temperature", "Unknown")
        humidity = current.get("humidity", "Unknown")
        descriptions = current.get("weather_descriptions") or []
        description = descriptions[0] if descriptions else "Unknown"

        return (
            f"City: {city}\n"
            f"Temperature: {temperature}°C\n"
            f"Weather: {description}\n"
            f"Humidity: {humidity}%"
        )

    except requests.RequestException as e:
        return f"Weather API request failed: {e}"

    except ValueError as e:
        return f"Invalid weather API response: {e}"


# ==========================================
# LLM: GEMINI
# ==========================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    temperature=0,
    api_key=GEMINI_API_KEY
)


# ==========================================
# REGISTER TOOLS
# ==========================================

tools = [
    search_tool,
    get_weather_data
]


# ==========================================
# CREATE AI AGENT
# ==========================================

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=(
        "You are a helpful AI assistant. "
        "Use Tavily when internet research is necessary. "
        "Use get_weather_data for live weather questions. "
        "Never invent current weather information. "
        "Answer clearly and concisely."
    )
)


# ==========================================
# RUN AGENT
# ==========================================

if __name__ == "__main__":

    user_query = (
        "Find the capital of India "
        "and then find its current weather."
    )

    print("\nUSER QUERY:")
    print(user_query)

    print("\n========== AGENT EXECUTION ==========\n")

    response = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": user_query
            }
        ]
    })

    print("\n========== FINAL ANSWER ==========\n")

    final_message = response["messages"][-1]
    print(final_message.content)
