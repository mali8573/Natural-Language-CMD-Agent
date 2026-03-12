import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("--- בודק רשימת מודלים זמינים ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"מודל זמין: {m.name}")
except Exception as e:
    print(f"שגיאה בחיבור: {e}")