import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('models/gemini-3-flash-preview')

try:
    print("בודק חיבור...")
    response = model.generate_content("say hello")
    print("תשובה מהמודל:", response.text)
except Exception as e:
    print("שגיאה שנמצאה:", e)