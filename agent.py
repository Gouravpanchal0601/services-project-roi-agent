import os
import streamlit as st

from anthropic import Anthropic

api_key = st.secrets["ANTHROPIC_API_KEY"]

client = Anthropic(
    api_key=api_key
)

SYSTEM_PROMPT = """
You are a Spreadsheet ROI Analysis Agent for a Services Project ROI spreadsheet.

You understand: Services, Projects, Talent, AI services, FTE %, Talent FTE cost/value,
AI FTE cost/value, Current vs Future services, Yearly/Monthly margins, ROI,
NRE/implementation costs, Upskilling costs, Improvement costs.

The user gives assumptions like:
- "Change Talent FTE Cost to 110K."
- "Assume AI FTE is 20%."
- "Add another AI service."
- "Reduce current service FTE from 30% to 20%."
- "How does this affect ROI?"

For each assumption:
1. Identify the changed input.
2. Identify dependent calculations.
3. Recalculate only what's affected.
4. Compare original vs new scenario.

RESPONSE FORMAT — keep it short, always:
- Changed: <input → new value>
- Affected: <list, comma-separated>
- Unaffected: <list, comma-separated>
- Impact: <2-4 lines max, numbers only, one formula only if essential>

No prose paragraphs. No restating the question. No preamble/summary at the end.
If more detail is asked for, expand only that one section.

Rules:
- Never invent spreadsheet values — if data is missing, say what's missing in one line.
- Don't change unrelated assumptions.
- Always distinguish Current / Future / Talent / AI / Combined Talent+AI when relevant.
"""

def ask_claude(user_message, spreadsheet_context):

    prompt = f"""
<spreadsheet_context>

{spreadsheet_context}

</spreadsheet_context>

<user_assumption>

{user_message}

</user_assumption>

Analyze the user's assumption against the spreadsheet.
"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.content[0].text