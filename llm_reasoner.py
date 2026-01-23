import os
from openai import OpenAI
from openai import RateLimitError, APIError

client = OpenAI()

def llm_reason(issue_type, analysis, resolution, ticket_context):
    prompt = f"""
You are a banking production support expert.

Issue Type: {issue_type}
Analysis: {analysis}
Resolution: {resolution}
Ticket Context: {ticket_context}

Provide a concise reasoning summary in a professional incident report tone.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return response.choices[0].message.content

    except (RateLimitError, APIError):
        return None  # 🔑 KEY FIX

    except Exception:
        return None  # 🔑 KEY FIX
