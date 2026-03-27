<!-- # Executive Data Co-Pilot 📊

An AI-powered Business Intelligence assistant that lets business leaders 
interact with sales data using plain English — no SQL knowledge required.

## What it does
- Ask questions in natural language → get instant charts and tables
- Every answer comes with a confidence score and transparency layer
- AI explains what happened, why, and what to do next
- Pin key insights to a personal saved board

## Tech Stack
- Frontend: Streamlit
- AI: Google Gemini API (gemma-3-27b-it)
- Data: SQLite (in-memory)
- Charts: Plotly
- Dataset: Superstore Sales

## How to run locally

### 1. Clone the repo
git clone https://github.com/PavelBodle/ai_bi_copilot.git
cd ai_bi_copilot

### 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Add your Gemini API key
Create a .env file in the root folder:
GEMINI_API_KEY=your_gemini_api_key_here

Get a free key at: https://aistudio.google.com

### 5. Add the dataset
Download Superstore Sales CSV from:
https://www.kaggle.com/datasets/vivek468/superstore-dataset-final

Save it as: data/superstore.csv

### 6. Run the app
streamlit run app.py

App will open at http://localhost:8501

## Live Demo
https://your-app-link.streamlit.app  ← update after deploy

## Author
Pavel Bodle
LinkedIn: https://www.linkedin.com/in/pavelbodle/
GitHub: https://github.com/PavelBodle -->

# AI-Powered Executive Data & BI Co-Pilot 📊

> A conversational Business Intelligence assistant that lets business leaders 
> query sales data in plain English — no SQL, no analyst queue, no waiting.

**Live Demo →** [https://your-app-link.streamlit.app](https://your-app-link.streamlit.app)  
*(update link after deploy)*

---

## The Problem This Solves

Business executives and sales leaders routinely need answers to questions like:
*"Which region had the worst Q3 margin?"* or *"What drove the spike in returns last month?"*

Today, getting those answers means filing a request with a data analyst, waiting hours or days, 
and often receiving a static chart that can't be followed up on. This creates a bottleneck 
at exactly the moment decisions need to be made.

**Who this is for:** Non-technical business leaders — VP Sales, Regional Directors, 
Finance Managers — who own outcomes but can't write SQL.

**Why it matters:** Faster decisions, fewer analyst bottlenecks, and a culture of 
data-driven thinking at every level of the business.

---

## What It Does

| Feature | Description |
|---|---|
| 💬 Natural Language Query | Type questions in plain English → get instant SQL-backed answers |
| 📊 Auto Visualization | AI selects the right chart type (bar, line, scatter, pie) for each question |
| 🔍 Confidence Score | Every answer is tagged with a confidence level so users know when to verify |
| 🧠 Insight Narrative | AI explains *what* happened, *why* it likely happened, and *what to do next* |
| 📌 Saved Insights Board | Pin key findings to a personal board for async sharing with your team |
| 🛡️ Transparency Layer | The generated SQL is always visible — users can audit exactly what was queried |

---

## Why AI Is Essential Here (Not Decorative)

The AI layer does three things a traditional BI dashboard cannot:

1. **Intent parsing** — It translates ambiguous business language ("worst performing region") 
   into precise, correct SQL without requiring the user to know schema or syntax.
2. **Contextual narration** — It generates a plain-English explanation of results, 
   including likely causes and recommended next steps, grounded in the data returned.
3. **Chart selection** — It automatically picks the most appropriate visualization 
   based on the shape and nature of the result set.

### Handling AI Limitations

- **Hallucination guard:** The SQL is always executed against the real database. 
  If the query fails or returns empty results, the AI is re-prompted to correct it 
  rather than fabricating an answer.
- **Confidence scoring:** The model assesses its own certainty and surfaces a 
  score (High / Medium / Low) so users know when to treat the answer as a starting 
  point rather than a final verdict.
- **Audit transparency:** The generated SQL is shown alongside every answer. 
  Business users can forward it to a data analyst for verification if needed.
- **Scope guardrails:** The system prompt constrains the AI to only query the 
  loaded dataset — it cannot browse the web or access external systems.

---

## Tech Stack

| Layer | Technology | Reason |
|---|---|---|
| Frontend | Streamlit | Fast to build, zero-friction sharing via Streamlit Cloud |
| AI | Google Gemini API (`gemma-3-27b-it`) | Strong reasoning + large context window for SQL + narrative generation |
| Database | SQLite (in-memory) | No server to manage; data loads from CSV at startup |
| Charts | Plotly | Interactive, embeds natively in Streamlit |
| Dataset | Kaggle Superstore Sales | Rich, realistic retail dataset with 9,994 orders across regions, categories, and time |

---

## Architecture Overview
