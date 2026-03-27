import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemma-3-27b-it")


def _clean_and_parse(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        parts = text.split("```")
        for part in parts:
            part = part.strip()
            if part.startswith("json"):
                part = part[4:].strip()
            try:
                return json.loads(part)
            except Exception:
                continue
    try:
        return json.loads(text)
    except Exception:
        return {"error": text}


def nl_to_sql(question: str, schema: str) -> dict:
    prompt = f"""You are a SQL expert. The database has one table called 'sales'.
Schema: {schema}

Convert this question to a valid SQLite query: {question}

Rules:
- Use only columns that exist in the schema above
- Always use table name 'sales'
- For date operations use SQLite date functions
- Keep the query simple and correct

Respond in raw JSON only with exactly two keys:
- sql: the SQLite query string
- assumptions: list of strings explaining any interpretations you made

Do not use markdown. Do not use code blocks. Return raw JSON only."""

    try:
        response = model.generate_content(prompt)
        return _clean_and_parse(response.text)
    except Exception as e:
        return {"error": str(e)}


def verify_trust(question: str, sql: str, result_summary: str) -> dict:
    prompt = f"""You are a data quality reviewer.

Question asked: {question}
SQL used: {sql}
Result summary: {result_summary}

Assess the reliability of this answer.
Respond in raw JSON only with exactly three keys:
- confidence: one of exactly these strings: high, medium, or low
- reason: one sentence explaining the confidence level
- flags: list of strings for any data concerns, empty list if none

Do not use markdown. Return raw JSON only."""

    try:
        response = model.generate_content(prompt)
        return _clean_and_parse(response.text)
    except Exception as e:
        return {"confidence": "medium", "reason": str(e), "flags": []}


def generate_insight(question: str, result_summary: str) -> dict:
    prompt = f"""You are a senior business analyst at a top consulting firm.

Business question: {question}
Data result: {result_summary}

Generate a concise, actionable business insight.
Respond in raw JSON only with exactly three keys:
- what: one sentence describing what the data shows
- why: one sentence on the likely business reason behind it
- next: one concrete action the business leader should take

Do not use markdown. Return raw JSON only."""

    try:
        response = model.generate_content(prompt)
        return _clean_and_parse(response.text)
    except Exception as e:
        return {"error": str(e)}