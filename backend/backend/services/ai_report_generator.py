from groq import Groq
import json
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_llm_report(context: dict) -> str:
    prompt = f"""
You are a senior credit underwriter.

Write a professional, well-structured AI Credit Evaluation Report.

Rules:
- Use clear headings
- Explain risk in simple language
- Do NOT invent numbers
- Do NOT contradict the decision
- Keep it concise and readable

SECTION: Business Overview
SECTION: Credit Profile
SECTION: Risk Assessment

DATA:
{json.dumps(context, indent=2)}

Output plain text only.
"""

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # ✅ SUPPORTED MODEL
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return completion.choices[0].message.content.strip()
