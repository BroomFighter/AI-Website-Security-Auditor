import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def explain_findings(findings: dict) -> str:
    # Convert findings dictionary into readable JSON string for the prompt
    formatted_findings = json.dumps(findings, indent=2)
    
    prompt = f"""
You are a top-tier cybersecurity auditor. 
Explain the following website security findings in plain, professional English for a non-technical audience:

{formatted_findings}

Provide:
1. Executive Summary
2. Key Security Risks
3. Recommendations to Fix Issues
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful cybersecurity auditing assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Could not generate AI explanation: {str(e)}"