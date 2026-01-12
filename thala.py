import google.generativeai as genai
import json

API_KEY = "AIzaSyDAodPnTZPB411VH6QUmX0IhalQTd2qcGo" # my gemini key is used please use yours for your work dont make me pay...
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_ai_command(user_text, current_source, current_dest):
    prompt = f"""
    You are a file organization assistant. Interpret the user's request.
    Current Source: {current_source}
    Current Destination Root: {current_dest}
    User Request: "{user_text}"

    Output JSON with these keys:
    1. "source_folder": (string) Path to use. Default to Current Source if not specified.
    2. "destination_folder_name": (string) Subfolder name (e.g., "Invoices"). Infer from context.
    3. "file_extensions": (list) e.g. [".pdf"] or ["*"].
    4. "time_filter_hours": (int) 0 for all/now, 24 for "old".
    5. "confirmation": (string) Brief summary of the plan.

    Output ONLY JSON.
    """
    try:
        response = model.generate_content(prompt)
        clean_text = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_text)
    except Exception as e:
        return {"error": str(e)}