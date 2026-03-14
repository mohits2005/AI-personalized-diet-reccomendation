An AI-powered diet recommendation web application that generates personalized meal plans, restaurant suggestions, and workout routines based on user health data and dietary preferences.

The system uses Large Language Models (LLMs) to analyze user inputs such as age, weight, diet type, allergies, and region to provide customized recommendations.

🚀 Features

Personalized diet recommendations

Restaurant suggestions based on dietary preference

Breakfast and dinner meal planning

Workout recommendations

Interactive web interface

AI-powered recommendations using LLMs

🛠️ Tech Stack

Backend

Python

FastAPI

LangChain

Groq API (Llama-3.3-70B)

Frontend

HTML

CSS

Jinja2 Templates

Other Tools

Regex (response parsing)

dotenv (environment variables)

⚙️ Installation
1️⃣ Clone the repository
git clone https://github.com/YOUR_USERNAME/AI-personalized-diet-reccomendation.git
2️⃣ Navigate to project
cd AI-personalized-diet-reccomendation
3️⃣ Create virtual environment
python -m venv diet
4️⃣ Activate environment

Windows:

diet\Scripts\activate

Linux / Mac:

source diet/bin/activate
5️⃣ Install dependencies
pip install fastapi uvicorn langchain langchain-groq python-dotenv jinja2
🔑 Environment Variables

Create a .env file in the root directory:

GROQ_API_KEY=your_api_key_here
▶️ Running the Application

Start the FastAPI server:

uvicorn app:app --reload

Open browser:

http://127.0.0.1:8000
📂 Project Structure
AI-personalized-diet-reccomendation
│
├── app.py
├── main.py
├── .env
├── .gitignore
│
├── templates
│   ├── index.html
│   └── result.html
│
└── diet (virtual environment)
📊 How It Works

User enters health and dietary details.

FastAPI backend processes the request.

LangChain sends prompt to Groq LLM (Llama-3.3-70B).

👨‍💻 Author

Mohit
Backend-focused Computer Science student passionate about AI and backend development.

AI generates diet, restaurant, and workout recommendations.

Response is parsed and displayed on the web interface.

