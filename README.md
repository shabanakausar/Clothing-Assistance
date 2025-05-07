# 🧵 AI Clothing Assistant
An intelligent clothing recommendation system that combines real-time weather data, user preferences, and inventory to suggest perfect outfits.

## ✨ Features

- **Personalized Recommendations**: Tailored suggestions based on your style and budget
- **Weather-Aware**: Considers real-time weather conditions for your location
- **Smart Inventory Search**: Finds matching items within your budget range
- **User Profiles**: Remembers preferences for returning users
- **Natural Language Interface**: Chat with the AI assistant conversationally

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI Backend**: LangChain + Groq (Llama3-8b)
- **Data**: OpenWeather API + Custom Inventory CSV
- **Memory**: ConversationBufferMemory

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Streamlit
- Groq API key
- OpenWeather API key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-clothing-assistant.git
   cd ai-clothing-assistant
Install dependencies:

bash
pip install -r requirements.txt
Create a .env file with your API keys:

env
GROQ_API_KEY=your_groq_key
OPENWEATHER_API_KEY=your_openweather_key
Prepare your inventory CSV (sample format):

csv
item,style,price
Denim Jacket,casual,89
Silk Blouse,formal,120
Running the App
bash
streamlit run app.py
🧩 Components
Core Tools
Weather Lookup: Gets real-time weather using OpenWeather API

Inventory Search: NLP-powered product search with style/budget filters

User Preferences: Personalized recommendations based on stored profiles

Agent Configuration
Chat-based conversational agent

Memory for context-aware conversations

Llama3-8b via Groq for fast inference

🖥️ UI Overview
Location Input: Auto-detected or manually entered

User Profile: Select from existing or use as guest

Style Selector: Choose your fashion aesthetic

Budget Slider: Set your spending limit

Chat Interface: Natural language conversation with the AI

📂 File Structure
.
├── app.py                # Main Streamlit application
├── clothing_inventory.csv # Sample product database
├── requirements.txt      # Python dependencies
└── README.md             # This documentation
🌟 Advanced Features
Dynamic budget range adjustment (±20% of selected budget)

Natural language parsing for inventory queries

IP-based location detection fallback

Cached inventory loading for performance

🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

📜 License
MIT


### Recommended Extras:
1. Add a `screenshot.png` of your UI
2. Create a `requirements.txt` with:
streamlit
langchain
langchain-groq
python-dotenv
pandas
requests


This README provides:
- Clear installation instructions
- Feature overview
- Technical architecture
- Visual representation
- Contribution guidelines
- License information

Would you like me to modify any section or add more details about specific components?
New chat

