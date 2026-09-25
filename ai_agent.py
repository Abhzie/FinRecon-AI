import os
from openai import OpenAI

def explain_exceptions(summary, exceptions):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return ("AI mode is not configured. Add OPENAI_API_KEY to enable "
                "natural-language exception analysis. Deterministic reconciliation "
                "results remain available.")
    client = OpenAI(api_key=api_key)
    prompt = f"""You are a finance transformation assistant. Use ONLY the supplied facts.
Do not invent accounting conclusions or financial advice.

Summary:
{summary}

Exception sample:
{exceptions}

Return:
1. Executive summary
2. Main exception drivers
3. Suggested investigation actions
"""
    response = client.responses.create(model="gpt-5-mini", input=prompt)
    return response.output_text
