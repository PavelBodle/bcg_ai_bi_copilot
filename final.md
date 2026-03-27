# AI-Powered Executive Data & BI Co-Pilot 📊

> A conversational Business Intelligence assistant that lets business leaders  
> query sales data in plain English: no SQL, no analyst queue, no waiting.

**Live URL (Demo) →** [https://pavelbodle-bcg.streamlit.app/](https://pavelbodle-bcg.streamlit.app/)

---

## The Problem This Solves

Business executives and sales leaders routinely need answers to questions like:
*"Which region had the worst Q3 margin?"* or *"What drove the spike in returns last month?"*

Today, getting those answers means filing a request with a data analyst, waiting hours or days, 
and often receiving a static chart that can't be followed up on. This creates a bottleneck 
at exactly the moment decisions need to be made.

**Who this is for:** Non-technical business leaders - VP Sales, Regional Directors,  
Finance Managers, who own outcomes but can't write SQL.

**Why it matters:** Faster decisions, fewer analyst bottlenecks, and a culture of 
data-driven thinking at every level of the business.

---

## What It Does


| Feature                   | Description                                                                    |
| ------------------------- | ------------------------------------------------------------------------------ |
| 💬 Natural Language Query | Type questions in plain English - get instant SQL-backed answers               |
| 📊 Auto Visualization     | AI selects the right chart type (bar, line, scatter, pie) for each question    |
| 🔍 Confidence Score       | Every answer is tagged with a confidence level so users know when to verify    |
| 🧠 Insight Narrative      | AI explains *what* happened, *why* it likely happened, and *what to do next*   |
| 📌 Saved Insights Board   | Pin key findings to a personal board for async sharing with your team          |
| 🛡️ Transparency Layer    | The generated SQL is always visible - users can audit exactly what was queried |


---

## Why AI Is Essential Here (Not Decorative)

The AI layer does three things a traditional BI dashboard cannot:

1. **Intent parsing**: It translates ambiguous business language ("worst performing region")
  into precise, correct SQL without requiring the user to know schema or syntax.
2. **Contextual narration**: It generates a plain-English explanation of results,
  including likely causes and recommended next steps, grounded in the data returned.
3. **Chart selection**:  It automatically picks the most appropriate visualization
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
loaded dataset - it cannot browse the web or access external systems.

---

## How Leaders Can Trust the Results

One of the biggest blockers to executive adoption of AI tools is a simple question:
**"How do I know this answer is correct?"**

This application addresses that directly through a **four-layer transparency system** — 
every response is designed to be auditable, not just readable.

### Layer 1:  Confidence Score Framework

Every answer is accompanied by a confidence rating (High / Medium / Low) with a 
plain-English explanation of *why* that confidence level was assigned.

> *"Confidence: High - The SQL query directly addresses the question by filtering for *  
> *loss-making transactions, grouping by sub-category, ordering by total loss, and *  
> *limiting to the top 5, which is a logical and efficient approach."*

This means a leader can immediately see whether the AI is certain or approximating -  
and decide whether to act on the result or escalate to an analyst.

### Layer 2: Assumptions Made Visible

The AI explicitly lists every assumption it made to interpret the question, no silent decisions.

> Example assumptions surfaced for *"What are the top 5 loss-making sub-categories?"*:
>
> - Loss-making is defined as having negative profit
> - The question asks for the sub-categories themselves, not aggregated values
> - We are looking for the top 5 sub-categories with the largest negative profit
> - `SUM(Profit)` is used to calculate total profit per sub-category

A senior manager can read these and immediately spot if the AI misunderstood intent,  
before the result influences a decision.

### Layer 3 : SQL Always Visible

The exact SQL query executed against the database is displayed alongside every result. 
This serves two purposes:

- **Verification:** Any data analyst on the team can review and confirm the query is logically correct
- **Auditability:** The result is not a black box — it is a deterministic query run 
against real data, not an AI-generated number

### Layer 4: Business Insight Narrative

Beyond raw data, the AI generates a structured three-part insight for every query:


| Card                   | What it answers                                                                                                              |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| **What happened**      | The factual finding from the data (e.g., *"Central region has 24% avg discount vs East's 15%"*)                              |
| **Why**                | The likely business reason behind the pattern (e.g., *"differing competitive pressures or promotional strategies"*)          |
| **Recommended action** | A concrete next step for the leader (e.g., *"Regional sales leader should investigate discounting impact on profitability"*) |


This mirrors how a trusted analyst would brief an executive, fact, context, and recommendation —  
rather than just dropping a chart.

> The goal is not to replace analyst judgment - it is to give leaders a  
> **verified first answer in seconds** so they know exactly what to escalate if needed.

---

## What I'd Improve With More Time

1. **Multi-turn memory** — Maintain conversation context so users can ask follow-up questions
  ("now break that down by sub-category") without re-stating full context.
2. **Semantic caching** — Cache semantically similar questions to reduce API latency and cost.
3. **Automated insight push** — Proactively surface anomalies (e.g., unusual spikes or drops)
  each morning without the user needing to ask.
4. **Role-based views** — Pre-configure dashboards per persona (e.g., CFO vs. Sales VP)
  so the starting context is always relevant.
5. **Production database connector** — Replace SQLite with a live Postgres/BigQuery
  connector so real enterprise data can be queried.

---

## How to Run Locally

### 1. Clone the repo

```bash
git clone https://github.com/PavelBodle/ai_bi_copilot.git
cd ai_bi_copilot
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your Gemini API key

Create a `.env` file in the root folder:

Get a free key at: [https://aistudio.google.com](https://aistudio.google.com)

### 5. Add the dataset

Download the Superstore Sales CSV from Kaggle:  
[https://www.kaggle.com/datasets/vivek468/superstore-dataset-final](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)

Save it as: `data/superstore.csv`  
*(The file is already included in this repo's `data/` folder.)*

### 6. Run the app

```bash
streamlit run app.py
```

App opens at [http://localhost:8501](http://localhost:8501)

---

## Example Questions to Try

"What are the top 5 loss-making sub-categories?"
"Top 3 products with highest sales?"
"Compare average discount by region"
"Which customer segment has the highest order volume?"
"Show monthly sales trend for the West region"

---

## Author

**Pavel Daulat Bodle**  
LinkedIn: [https://www.linkedin.com/in/pavelbodle/](https://www.linkedin.com/in/pavelbodle/)  
GitHub: [https://github.com/PavelBodle](https://github.com/PavelBodle)