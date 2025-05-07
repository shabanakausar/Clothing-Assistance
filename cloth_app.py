#Streamlit app: an upgraded AI Clothing Assistant with:

#✅ Dropdown for style
#✅ Slider for budget
#✅ Name input (optional memory prep)
#✅ Chat UI with st.chat_message()
#✅ Real weather + inventory + preferences
#✅ Agent powered by LangChain + Groq LLaMA3

# app.py

import os
import re
import requests
import streamlit as st
import requests
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import Tool, initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain.agents.agent_types import AgentType
from langchain.tools import tool
import pandas as pd

# Load environment variables
load_dotenv()

# ========== Configuration ==========
st.set_page_config(page_title="🧵 AI Clothing Assistant", page_icon="🧠")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not OPENWEATHER_API_KEY or not GROQ_API_KEY:
    st.error("Please set your OpenWeather and Groq API keys in the environment variables.")

def get_user_city_by_ip():
    try:
        res = requests.get("https://ipinfo.io/json")
        if res.status_code == 200:
            data = res.json()
            return data.get("city", "New York")
    except Exception as e:
        return "New York"  # fallback default


# ========== Mock Databases ==========
@st.cache_data
def load_inventory():
    return pd.read_csv("clothing_inventory.csv")

inventory_df = load_inventory()

#----------- User Preferences --------------
user_preferences = {
    "alex": {"style": "minimalist", "budget": 200},
    "jamie": {"style": "boho", "budget": 150},
}

# =================== Tools =================

@tool
def get_weather(location: str) -> str:
    """Get real weather data for a location."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        res = requests.get(url)
        data = res.json()
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"The weather in {location} is {temp}°C with {weather}."
    except Exception as e:
        return f"Failed to get weather for {location}: {str(e)}"

@tool
def lookup_inventory(input: str) -> str:
    """
    Look up inventory using natural language input.
    Parses style, budget, and item keywords.
    """

    style_keywords = ["minimalist", "boho", "casual", "formal", "sporty"]
    detected_style = next((style for style in style_keywords if style in input.lower()), "casual")

    budget_match = re.search(r"\$?(\d{2,4})", input)
    budget = int(budget_match.group(1)) if budget_match else 100
    budget_range = (budget - 20, budget + 20)

    item_keywords = ["jacket", "dress", "suit", "shirt", "tee", "shoes", "sneakers", "coat", "bag", "poncho", "tie"]
    found_item = next((item for item in item_keywords if item in input.lower()), None)

    # Filter DataFrame
    df = inventory_df.copy()
    df = df[df["style"] == detected_style]
    df = df[df["price"] <= budget]

    if found_item:
        df = df[df["item"].str.contains(found_item, case=False)]

    if df.empty:
        return f"No items found for style '{detected_style}' within budget ${budget}."
    
    return "\n".join([f"{row['item']} - ${row['price']}" for _, row in df.iterrows()])


@tool
def load_user_preferences(username: str) -> str:
    """Load a user's preferred style and budget."""
    prefs = user_preferences.get(username.lower(), {"style": "casual", "budget": 100})
    return f"Style: {prefs['style']}, Budget: ${prefs['budget']}"

# ========== Agent Setup ==========
llm = ChatGroq(temperature=0, model="Llama3-8b-8192")


tools = [
    Tool.from_function(get_weather,
        name="get_weather",
        description="Get the current weather for a given location."),
    Tool.from_function(lookup_inventory,
        name="Lookup Inventory",
        description="Use this tool to look up products in the inventory by name."),
    Tool.from_function(load_user_preferences,
        name="Load User Preferences",
        description="Load user preferences for style and budget."),
]

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    memory=memory,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
)

# ========== Streamlit UI ==========
st.title("🦜️🔗 AI Clothing Assistant")
st.write("Ask for outfit recommendations based on weather, preferences, and budget.")

# Preferences UI
default_city = get_user_city_by_ip()
location = st.text_input("Detected your city (you can change it):", default_city)
username = st.selectbox("Select User:", list(user_preferences.keys()) + ["guest"])
style = st.selectbox("Select style:", ["minimalist", "boho", "casual","formal", "sporty"])
budget = st.slider("Select budget:", 10,  300, 150, step=2)
 
# Chat input
if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.text_input("Ask a question:", placeholder = "Suggest an outfit for me.")

weather_summary = get_weather(location)
if user_input:
    prompt = (
        f"I'm {username}, planning an outfit in {location}. "
        f"The weather there is {weather_summary.lower()}. "
        f"My aesthetic is {style}, and my budget is ${budget}. "
        f"{user_input} What outfit would you suggest that fits both the vibe and the weather?"
    )
    response = agent.run(prompt)
    st.session_state.chat.append(("🧑", user_input))
    st.session_state.chat.append(("🤖", response))

# Show chat history
for role, msg in st.session_state.chat:
    st.markdown(f"**{role}**: {msg}")
