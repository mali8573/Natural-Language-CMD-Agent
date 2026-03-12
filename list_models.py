import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("בודק מודלים זמינים עבור המפתח שלך...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"שם המודל: {m.name}")
except Exception as e:
    print(f"שגיאה בגישה לרשימה: {e}")