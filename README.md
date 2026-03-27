# Executive Data Co-Pilot 📊

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
GitHub: https://github.com/PavelBodle