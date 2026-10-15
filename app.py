
import os
import certifi
import requests
import streamlit as st

from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langchain_core.messages import HumanMessage, AIMessage


# ==========================================
# STREAMLIT CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Moneeb Agentic AI Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Moneeb Agentic AI Assistant")
st.caption("Powered by Gemini, LangChain, Tavily & Weatherstack")


# ==========================================
# ENVIRONMENT VARIABLES
# ==========================================

os.environ["SSL_CERT_FILE"] = certifi.where()
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API_KEY")

missing_keys = [
    name for name, value in {
        "GEMINI_API_KEY": GEMINI_API_KEY,
        "TAVILY_API_KEY": TAVILY_API_KEY,
        "WEATHERSTACK_API_KEY": WEATHERSTACK_API_KEY
    }.items() if not value
]

if missing_keys:
    st.error(
        "Missing API keys in .env: "
        + ", ".join(missing_keys)
    )
    st.stop()


# ==========================================
# TOOL 1: INTERNET SEARCH
# ==========================================

search_tool = TavilySearch(
    max_results=3
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
            return f"Weather unavailable for {city}: {error}"

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
        return f"Invalid weather response: {e}"


# ==========================================
# CREATE GEMINI AGENT
# ==========================================

@st.cache_resource
def initialize_agent():

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        temperature=0,
        api_key=GEMINI_API_KEY
    )

    tools = [
        search_tool,
        get_weather_data
    ]

    return create_agent(
        model=llm,
        tools=tools,
        system_prompt=(
            "You are a helpful AI assistant. "
            "Answer the user's questions accurately. "
            "Use Tavily for information that requires internet search. "
            "Use get_weather_data to retrieve current weather. "
            "Do not invent live weather information. "
            "Use the conversation history to understand follow-up questions. "
            "Provide clear, friendly answers."
        )
    )


agent = initialize_agent()


# ==========================================
# CHAT HISTORY
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.header("⚙️ Settings")

    show_steps = st.checkbox(
        "Show agent execution steps",
        value=False
    )

    if st.button("🗑️ Clear conversation"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.subheader("🛠️ Available Tools")
    st.write("🔎 Tavily Web Search")
    st.write("🌤️ Weatherstack Weather API")

    st.divider()
    st.caption("LLM: Gemini 3.8 Flash")


# ==========================================
# USER INPUT
# ==========================================

user_query = st.chat_input(
    "Ask me anything..."
)


# ==========================================
# RUN AGENT
# ==========================================

if user_query:

    st.session_state.messages.append({
        "role": "user",
        "content": user_query
    })

    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):

        with st.spinner("Agent is thinking..."):

            try:

                # Convert Streamlit history to LangChain messages
                conversation = []

                for message in st.session_state.messages:

                    if message["role"] == "user":
                        conversation.append(
                            HumanMessage(content=message["content"])
                        )

                    elif message["role"] == "assistant":
                        conversation.append(
                            AIMessage(content=message["content"])
                        )

                response = agent.invoke({
                    "messages": conversation
                })

                final_message = response["messages"][-1]

                if isinstance(final_message.content, str):
                    answer = final_message.content
                else:
                    answer = "\n".join(
                        block["text"]
                        for block in final_message.content
                        if isinstance(block, dict)
                        and block.get("type") == "text"
                    )

                # Display answer
                if isinstance(answer, str):
                    st.markdown(answer)
                    saved_answer = answer
                else:
                    saved_answer = str(answer)
                    st.write(answer)

                # Optional execution trace
                if show_steps:

                    with st.expander("🔍 Agent execution steps"):

                        for message in response["messages"]:

                            tool_calls = getattr(
                                message,
                                "tool_calls",
                                None
                            )

                            if tool_calls:
                                for call in tool_calls:
                                    st.write(
                                        f"🔧 Tool called: {call['name']}"
                                    )
                                    st.json(call["args"])

                            if message.type == "tool":
                                st.write(
                                    f"✅ Tool result ({message.name})"
                                )
                                st.code(str(message.content))

                # Save answer
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": saved_answer
                })

            except Exception as e:

                st.error(f"An error occurred: {e}")
