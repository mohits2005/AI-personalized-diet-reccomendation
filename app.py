from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import LLMChain
from langchain_groq import ChatGroq
import os
import re
import asyncio
from dotenv import load_dotenv
app = FastAPI()


load_dotenv()
# Serve files from ./static if you have CSS/JS; optional
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 templates folder (same as Flask's templates)
templates = Jinja2Templates(directory="templates")

# === LLM setup (use environment variable for the API key) ===
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # set this in your environment, e.g. export GROQ_API_KEY="sk_..."
if not GROQ_API_KEY:
    # warning only — in production you should raise or log more clearly
    print("WARNING: GROQ_API_KEY is not set. Set the environment variable before running.")

llm_resto = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.3-70b-versatile",
    temperature=0.0
)

prompt_template_resto = PromptTemplate(
    input_variables=[
        'age', 'gender', 'weight', 'height', 'veg_or_nonveg',
        'disease', 'region', 'allergics', 'foodtype'
    ],
    template=(
        "Diet Recommendation System:\n"
        "I want you to provide output in the following format using the input criteria:\n\n"
        "Restaurants:\n"
        "- name1\n- name2\n- name3\n- name4\n- name5\n- name6\n\n"
        "Breakfast:\n"
        "- item1\n- item2\n- item3\n- item4\n- item5\n- item6\n\n"
        "Dinner:\n"
        "- item1\n- item2\n- item3\n- item4\n- item5\n\n"
        "Workouts:\n"
        "- workout1\n- workout2\n- workout3\n- workout4\n- workout5\n- workout6\n\n"
        "Criteria:\n"
        "Age: {age}, Gender: {gender}, Weight: {weight} kg, Height: {height} ft, "
        "Vegetarian: {veg_or_nonveg}, Disease: {disease}, Region: {region}, "
        "Allergics: {allergics}, Food Preference: {foodtype}.\n"
    )
)

# GET route to show form (index.html should be in templates/)
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# POST route to receive form data and return the result page
@app.post("/recommend", response_class=HTMLResponse)
async def recommend(
    request: Request,
    age: str = Form(...),
    gender: str = Form(...),
    weight: str = Form(...),
    height: str = Form(...),
    veg_or_nonveg: str = Form(...),
    disease: str = Form(...),
    region: str = Form(...),
    allergics: str = Form(...),
    foodtype: str = Form(...)
):
    # Build the LangChain LLMChain
    chain = LLMChain(llm=llm_resto, prompt=prompt_template_resto)

    # Prepare input_data (keep strings as earlier; convert types if needed)
    input_data = {
        'age': age,
        'gender': gender,
        'weight': weight,
        'height': height,
        'veg_or_nonveg': veg_or_nonveg,
        'disease': disease,
        'region': region,
        'allergics': allergics,
        'foodtype': foodtype
    }

    # chain.run may be synchronous depending on your LangChain version;
    # run it in a thread to avoid blocking the event loop.
    results = await asyncio.to_thread(chain.run, input_data)

    # Extract blocks using regex (same as your original approach)
    restaurant_names = re.findall(r'Restaurants:\s*(.*?)\n\n', results, re.DOTALL)
    breakfast_names = re.findall(r'Breakfast:\s*(.*?)\n\n', results, re.DOTALL)
    dinner_names = re.findall(r'Dinner:\s*(.*?)\n\n', results, re.DOTALL)
    workout_names = re.findall(r'Workouts:\s*(.*?)\n\n', results, re.DOTALL)

    # Cleaning helper (same functionality as yours)
    def clean_list(block):
        # split into lines, strip bullet '-' and surrounding whitespace, ignore empty lines
        return [line.strip().lstrip("-").strip() for line in block.strip().split("\n") if line.strip()]

    restaurant_names = clean_list(restaurant_names[0]) if restaurant_names else []
    breakfast_names = clean_list(breakfast_names[0]) if breakfast_names else []
    dinner_names = clean_list(dinner_names[0]) if dinner_names else []
    workout_names = clean_list(workout_names[0]) if workout_names else []

    # Render result.html (make sure this exists in templates/)
    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "restaurant_names": restaurant_names,
            "breakfast_names": breakfast_names,
            "dinner_names": dinner_names,
            "workout_names": workout_names,
        },
    )

# Run with: uvicorn app_fastapi:app --reload
# (or put the following block under `if __name__ == "__main__":` to run as script)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
