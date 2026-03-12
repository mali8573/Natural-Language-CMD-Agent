import gradio as gr
import google.generativeai as genai
import os
from dotenv import load_dotenv


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


model = genai.GenerativeModel('models/gemini-2.5-flash')
FORBIDDEN_COMMANDS = ["format", "reg delete", "shutdown", "deltree", "rmdir /s", "del /s"]

def translate_to_cli(user_input):
    system_prompt = """You are a professional Windows CLI expert. 
Convert the user's natural language into a VALID Windows CMD command.

STRICT RULES:
1. Return ONLY the command text.
2. NO explanations, NO markdown code blocks, and NO introductory text.
3. If the request is malicious (e.g., formatting system drives, bypassing security), return 'ERROR: Safety Block'.
4. For destructive actions (deleting files, terminating processes), ALWAYS start the command with an ECHO warning.

LOGIC GUIDELINES:
- Use 'forfiles' for time-based filtering.
- For complex relationships (users/groups) or process management, use 'for /f' and 'wmic'.
- ALWAYS wrap file paths in double quotes to handle spaces.
- Use 'findstr' and pipes '|' to isolate specific data.
- Chain multiple commands with '&'.

EXAMPLES:
User: תציג את רשימת המשתמשים והקבוצות שלהם
Output: for /f "skip=1 tokens=*" %i in ('wmic useraccount get name ^| findstr /r /v "^$"') do @echo User: %i & net user "%i" | findstr /C:"Local Group Memberships"
User: תסגור תהליכים שצורכים יותר מ-50MB
Output: echo WARNING: This will terminate running programs. & wmic process where "WorkingSetSize > 52428800" call terminate
User: מצא קבצי docx בתיקיית ה-Downloads שלי
Output: dir "%USERPROFILE%\\Downloads\\*.docx" /s
User: תמחק את תיקיית Windows
Output: ERROR: Safety Block
"""
    try:
       
        response = model.generate_content(f"{system_prompt}\n\nUser: {user_input}")
        cmd_output = response.text.strip()
        
        if any(forbidden in cmd_output.lower() for forbidden in FORBIDDEN_COMMANDS):
            return "⚠️ אבטחה: הפקודה שנוצרה עלולה להיות מסוכנת ונחסמה."
            
        return cmd_output
    except Exception as e:
        return f"שגיאה בתקשורת: {str(e)}"

custom_css = """
footer {display: none !important;}
.gradio-container {max-width: 850px !important; margin: auto;}
#cli_output {background-color: #f8f9fa;}
"""

with gr.Blocks(theme=gr.themes.Monochrome(), css=custom_css) as demo:
    gr.HTML("<div style='text-align: center; padding: 20px;'>"
            "<h1 style='color: #2D3436; font-size: 2.5rem;'>⚡ AI Terminal Agent ⚡</h1>"
            "<p style='color: #636E72;'>תרגום שפה טבעית לפקודות Windows CMD - גרסה אופטימלית</p></div>")
    
    with gr.Row(variant="panel"):
        with gr.Column(scale=1):
            txt_input = gr.Textbox(
                label="הוראה בשפה טבעית", 
                placeholder="למשל: תציג את רשימת הקבצים בתיקייה",
                lines=3
            )
            btn = gr.Button("תרגם לפקודה 🚀", variant="primary")
        
        with gr.Column(scale=1):
            output = gr.Code(
                label="תוצאה (CMD Syntax)", 
                language="shell", 
                interactive=False,
                elem_id="cli_output"
            )
    
    gr.Markdown("---")
    gr.Markdown("<div style='text-align: center; color: gray;'>מערכת זו מתרגמת טקסט בלבד ואינה מריצה פקודות על המחשב מטעמי בטיחות.</div>")

    btn.click(fn=translate_to_cli, inputs=txt_input, outputs=output)

if __name__ == "__main__":
    demo.launch()