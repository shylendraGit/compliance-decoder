# === Begin File: backend/utils/gpt_analyzer.py ===
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("GPT_API_KEY"))

SYSTEM_PROMPT = """
You are a regulatory risk assistant. Given the extracted text of a supplier certificate, identify any potential issues.
Return a JSON object with:
- risk_level: Low, Medium, or High
- flags: a list of specific concerns
- summary: a one-paragraph plain-English explanation
"""

def analyze_certificate_text(text: str) -> dict:
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text}
            ],
            temperature=0.3,
            max_tokens=400,
        )
        output = response.choices[0].message.content
        return eval(output) if output.startswith("{") else {"summary": output}
    except Exception as e:
        return {"error": str(e)}
# === End File: backend/utils/gpt_analyzer.py ===
