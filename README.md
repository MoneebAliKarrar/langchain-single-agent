# langchain-single-agent
# 🤖 Agentic AI Assistant

An intelligent AI assistant built with **LangChain, Google Gemini, Streamlit, Tavily Search, and Weatherstack API**.

This project demonstrates how to build an **AI agent capable of using external tools, retrieving real-time information, and answering user queries through an interactive web interface**.

Unlike a traditional chatbot, this assistant can decide when to use external tools and incorporate their results into its responses.

## 🚀 Features

- **AI-Powered Reasoning:** Uses Google Gemini to understand queries and select appropriate tools.
- **Real-Time Web Search:** Integrates Tavily Search to retrieve information from the internet.
- **Live Weather Information:** Uses the Weatherstack API to fetch current weather conditions.
- **Autonomous Tool Selection:** Uses LangChain agents to select and execute tools based on user requests.
- **Interactive Chat Interface:** Built with Streamlit for a simple, user-friendly experience.
- **Conversation History:** Maintains chat context during the Streamlit session.
- **Agent Execution Monitoring:** Optionally displays tool calls and their results.

## 🧠 How It Works

The assistant follows an agentic workflow:

```text
                  User Query
                      |
                      v
              Streamlit Interface
                      |
                      v
                LangChain Agent
                      |
                      v
                 Gemini LLM
                      |
                      v
               Tool Selection
                 /         \
                v           v
          Tavily Search   Weatherstack
                \           /
                 v         v
                 Tool Results
                      |
                      v
                   Gemini
                      |
                      v
                Final Response
                      |
                      v
              Streamlit Interface
```

The Gemini model determines whether external information is needed. LangChain executes the selected tools and passes their results back to Gemini, which generates the final response.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| LangChain | Agent orchestration and tool integration |
| LangGraph | Underlying agent execution framework |
| Google Gemini | Large Language Model (LLM) |
| Tavily Search | Web search and information retrieval |
| Weatherstack API | Real-time weather information |
| Streamlit | Interactive web application |
| Python-dotenv | Environment variable management |

## 📁 Project Structure

```text
langchain-single-agent/
│
├── main.py
├── app.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

- `main.py` — Runs the AI agent directly in the terminal.
- `app.py` — Provides the Streamlit chat interface.
- `requirements.txt` — Lists Python dependencies.
- `.env` — Stores API keys locally (not committed to GitHub).
- `.gitignore` — Excludes sensitive and unnecessary files.
- `README.md` — Project documentation.

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/MoneebAliKarrar/langchain-single-agent.git

cd langchain-single-agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

For Linux/macOS:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

The project uses the following main packages:

```text
langchain>=1.0,<2.0
langchain-google-genai>=3.0
langchain-tavily
streamlit
requests
python-dotenv
certifi
```

## 🔑 API Configuration

The application requires three API keys:

1. **Google Gemini API** — [Google AI Studio](https://aistudio.google.com/)
2. **Tavily Search API** — [Tavily](https://www.tavily.com/)
3. **Weatherstack API** — [Weatherstack](https://weatherstack.com/)

Create a `.env` file in the project's root directory:

```env
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
WEATHERSTACK_API_KEY=your_weatherstack_api_key
```

**Security:** Never commit your `.env` file or expose API keys in your public repository.

## ▶️ Running the Application

### Option 1: Run the terminal agent

```bash
python main.py
```

The terminal version runs a predefined query and prints the generated response.

### Option 2: Run the Streamlit web application

```bash
python -m streamlit run app.py
```

Open your browser at:

http://localhost:8501

The application provides an interactive chat interface for asking questions and interacting with the agent.

## 💬 Example Queries

**Weather Information**

> What is the capital of Sudan, and what is its current weather?

**Web Search**

> Search for the latest developments in artificial intelligence.

**Multi-Step Tool Usage**

> Find the capital cities of Germany and France, then compare their current weather conditions.

**Follow-Up Questions**

> What about the capital of Italy?

The assistant uses conversation history to interpret follow-up questions during the active Streamlit session.

## 🧩 Custom Tools

The application includes a custom weather tool created using LangChain's `@tool` decorator.

```python
from langchain.tools import tool
import requests

@tool
def get_weather_data(city: str) -> str:
    """Fetch current weather information for a city."""

    response = requests.get(
        "https://api.weatherstack.com/current",
        params={
            "access_key": WEATHERSTACK_API_KEY,
            "query": city
        },
        timeout=15
    )

    response.raise_for_status()
    data = response.json()

    if "current" not in data:
        return f"Weather unavailable for {city}"

    current = data["current"]

    return (
        f"City: {city}\n"
        f"Temperature: {current['temperature']}°C\n"
        f"Humidity: {current['humidity']}%"
    )
```

LangChain allows custom Python functions to be exposed to the LLM as tools, enabling the agent to interact with external APIs.

## 🔮 Future Improvements

- [ ] Add more tools for travel planning and general information retrieval.
- [ ] Implement persistent conversation memory.
- [ ] Add structured logging and agent execution tracing.
- [ ] Improve API error handling and fallback behavior.
- [ ] Add streaming responses in the Streamlit interface.
- [ ] Deploy the application online.

## 🎯 Project Purpose

This project was developed as a hands-on introduction to **Agentic AI development**.

It explores important concepts such as:

- Large Language Models (LLMs)
- Tool calling and function execution
- Agent orchestration
- External API integration
- Multi-step agent workflows
- Conversation state management
- Building AI-powered applications with Python

## 📄 License

No license has been specified for this repository.

## 👨‍💻 Author

**Moneeb Ali Karrar**

GitHub: [@MoneebAliKarrar](https://github.com/MoneebAliKarrar)

---

Built with Python, LangChain, Google Gemini, and Streamlit.
