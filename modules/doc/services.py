import os
import base64
import json
from openai import OpenAI
from pydantic import BaseModel
from typing import List

# =========================
# PYDANTIC MODELS
# =========================
class CareTask(BaseModel):
    task: str
    priority: str
    timing: str
    notes: str

class CaretakerTodo(BaseModel):
    patient_name: str
    diagnosis: str
    medications: List[CareTask]
    daily_care: List[CareTask]
    caretaker_todo: List[CareTask]
    diet_instructions: List[str]
    warning_signs: List[str]
    follow_up: List[str]

# =========================
# HELPER / AI FUNCTIONS
# =========================
def get_openai_client():
    """Initializes client safely ensuring env vars are loaded."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing from the .env file.")
    return OpenAI(
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key=api_key,
    )

def get_image_data_url(image_file: str, image_format: str) -> str:
    try:
        with open(image_file, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not read '{image_file}'.")
    return f"data:image/{image_format};base64,{image_data}"

def generate_todo(image_path: str) -> dict:
    client = get_openai_client()
    schema = CaretakerTodo.model_json_schema()

    prompt = f"""
You are an intelligent medical caretaker assistant.
Analyze this medical report, prescription, or medical document image carefully.
Generate a structured caretaker TO-DO list for the patient's caregiver.
Return ONLY valid JSON matching this schema:

{json.dumps(schema, indent=2)}

Instructions:
- Keep all tasks simple and actionable.
- Create a separate caretaker_todo section with the main actions a caregiver should take.
- Include medication reminders, mobility or daily care support, diet guidance, monitoring, and follow-up coordination.
- Write at least 5 caregiver tasks when possible.
- Each caretaker task should include a clear task title, priority, timing, and a detailed note describing why and how to do it.
- Use the following style examples for content:
  - Assist with Walking and Mobility
  - Monitor Knee and Back Pain
  - Prevent Lower Back Strain
  - Ensure Medicines are Taken
  - Encourage Hydration
  - Watch for Worsening Symptoms
- Medicines should include timing and importance.
- Mention diet recommendations if available.
- Mention warning signs to monitor.
- Mention follow-up tests or doctor visits.
- If information is unavailable, use "N/A".
- Do not wrap response in markdown.
"""

    ext = image_path.rsplit('.', 1)[-1].lower()
    img_format = "jpeg" if ext in ("jpg", "jpeg") else "png"

    response = client.beta.chat.completions.parse(
        model="gemini-flash-lite-latest",
        response_format=CaretakerTodo,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful medical caretaker assistant."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": get_image_data_url(image_path, img_format),
                            "detail": "high"
                        }
                    }
                ]
            }
        ]
    )

    result = response.choices[0].message.parsed
    result_json = json.dumps(result, default=lambda o: o.__dict__, indent=2)
    return json.loads(result_json)