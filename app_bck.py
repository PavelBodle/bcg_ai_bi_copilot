import streamlit as st
import plotly.express as px
import pandas as pd

from db import load_data, run_query, get_schema
from ai import nl_to_sql, verify_trust, generate_insight

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    # page_title="Executive Data & AI BI Dashboard Co-Pilot",
    page_title="AI-Powered Executive Data & BI Co-Pilot",
    page_icon="🤖",
    layout="wide"
)

# ── Session state init ────────────────────────────────────────────────────────
if "pinned" not in st.session_state:
    st.session_state["pinned"] = []
if "current" not in st.session_state:
    st.session_state["current"] = None
if "current_insight" not in st.session_state:
    st.session_state["current_insight"] = None

# ── Load data once ────────────────────────────────────────────────────────────
@st.cache_resource
def get_connection():
    conn, df = load_data("data/superstore.csv")
    schema = get_schema(conn)
    return conn, df, schema

conn, df, schema = get_connection()

# ── Helper: confidence badge ──────────────────────────────────────────────────
def show_confidence(confidence: str, reason: str):
    if confidence == "high":
        st.success(f"✅ Confidence: High — {reason}")
    elif confidence == "medium":
        st.warning(f"⚠️ Confidence: Medium — {reason}")
    else:
        st.error(f"🔴 Confidence: Low — {reason}")

# ── Helper: build result summary string ──────────────────────────────────────
def build_summary(result_df: pd.DataFrame) -> str:
    return (
        f"{len(result_df)} rows returned. "
        f"Columns: {list(result_df.columns)}. "
        f"Sample: {result_df.head(2).to_dict()}"
    )

# ── Helper: auto chart from dataframe ────────────────────────────────────────
def auto_chart(result_df: pd.DataFrame, title: str = "Result"):
    if result_df.empty:
        return
    num_cols = result_df.select_dtypes(include="number").columns.tolist()
    cat_cols = result_df.select_dtypes(exclude="number").columns.tolist()
    if num_cols and cat_cols:
        fig = px.bar(
            result_df,
            x=cat_cols[0],
            y=num_cols[0],
            title=title,
            color_discrete_sequence=["#4F86C6"]
        )
        fig.update_layout(margin=dict(t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)
    elif len(num_cols) >= 2:
        fig = px.line(
            result_df,
            x=num_cols[0],
            y=num_cols[1],
            title=title
        )
        st.plotly_chart(fig, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════════
# SECTION 1 — Header + Auto Dashboard
# ════════════════════════════════════════════════════════════════════════════════
st.title("📊 Executive Data Co-Pilot")
st.caption("Ask your business data anything — powered by Gemini AI")

st.divider()

# KPI cards
col1, col2, col3 = st.columns(3)

total_sales = df["Sales"].sum()
total_orders = len(df)
avg_margin = (df["Profit"] / df["Sales"]).mean() * 100

col1.metric("💰 Total Sales", f"${total_sales/1_000_000:.2f}M")
col2.metric("📦 Total Orders", f"{total_orders:,}")
col3.metric("📈 Avg Profit Margin", f"{avg_margin:.1f}%")

# Auto chart — Sales by Region
st.subheader("Sales by Region")
region_df = df.groupby("Region")["Sales"].sum().reset_index()
fig_region = px.bar(
    region_df,
    x="Region",
    y="Sales",
    color="Region",
    title="Total Sales by Region",
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig_region.update_layout(showlegend=False, margin=dict(t=40, b=20))
st.plotly_chart(fig_region, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════════
# SECTION 2 — Ask Anything
# ════════════════════════════════════════════════════════════════════════════════
st.divider()
st.subheader("🤖 Ask Anything")

question = st.text_input(
    "Ask a question about your data",
    placeholder="e.g. Which region had the highest profit last year?",
    key="question_input"
)

ask_clicked = st.button("Ask", type="primary")

if ask_clicked and question.strip():
    with st.spinner("Thinking..."):

        # Step 1 — NL to SQL
        sql_result = nl_to_sql(question, schema)

        if "error" in sql_result:
            st.error(f"Could not generate SQL: {sql_result['error']}")
        else:
            sql = sql_result.get("sql", "")
            assumptions = sql_result.get("assumptions", [])

            # Step 2 — Run query
            result = run_query(conn, sql)

            if isinstance(result, str):
                st.error(f"Query failed: {result}")
                with st.expander("See SQL that failed"):
                    st.code(sql, language="sql")

            elif isinstance(result, pd.DataFrame):

                # Step 3 — Trust verification
                summary = build_summary(result)
                trust = verify_trust(question, sql, summary)

                confidence = trust.get("confidence", "medium")
                reason = trust.get("reason", "")
                flags = trust.get("flags", [])

                # Show confidence badge
                show_confidence(confidence, reason)

                # Show assumptions
                if assumptions:
                    st.info("💡 Assumptions made: " + " · ".join(assumptions))

                # Show flags
                if flags:
                    st.warning("⚠️ Data flags: " + " · ".join(flags))

                # Show result table
                st.dataframe(result, use_container_width=True)

                # Show chart
                auto_chart(result, title=question)

                # Show SQL
                with st.expander("🔍 See SQL query"):
                    st.code(sql, language="sql")

                # Store in session state
                st.session_state["current"] = {
                    "question": question,
                    "sql": sql,
                    "result": result,
                    "summary": summary,
                    "confidence": confidence,
                    "reason": reason,
                }
                st.session_state["current_insight"] = None


# Generate Insight button — only show if we have a current result
if st.session_state["current"]:
    st.divider()

    if st.button("✨ Generate Insight", type="secondary"):
        with st.spinner("Generating insight..."):
            current = st.session_state["current"]
            insight = generate_insight(
                current["question"],
                current["summary"]
            )
            st.session_state["current_insight"] = insight

    if st.session_state["current_insight"]:
        insight = st.session_state["current_insight"]

        if "error" in insight:
            st.error(f"Insight error: {insight['error']}")
        else:
            st.markdown("#### 🧠 Business Insight")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.info(f"**What happened**\n\n{insight.get('what', '—')}")
            with col_b:
                st.info(f"**Why**\n\n{insight.get('why', '—')}")
            with col_c:
                st.info(f"**Recommended action**\n\n{insight.get('next', '—')}")


# ════════════════════════════════════════════════════════════════════════════════
# SECTION 3 — Pin & Saved Insights
# ════════════════════════════════════════════════════════════════════════════════
if st.session_state["current"] and st.session_state["current_insight"]:
    if "error" not in st.session_state["current_insight"]:
        if st.button("📌 Pin this insight"):
            current = st.session_state["current"]
            insight = st.session_state["current_insight"]
            st.session_state["pinned"].append({
                "question": current["question"],
                "confidence": current["confidence"],
                "reason": current["reason"],
                "what": insight.get("what", ""),
                "why": insight.get("why", ""),
                "next": insight.get("next", ""),
            })
            st.success("Insight pinned!")

st.divider()
st.subheader("📌 Saved Insights")

if not st.session_state["pinned"]:
    st.caption("No insights pinned yet. Ask a question and pin insights you find useful.")
else:
    for i, pin in enumerate(reversed(st.session_state["pinned"])):
        with st.expander(f"❓ {pin['question']}"):
            show_confidence(pin["confidence"], pin["reason"])
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info(f"**What happened**\n\n{pin['what']}")
            with col2:
                st.info(f"**Why**\n\n{pin['why']}")
            with col3:
                st.info(f"**Recommended action**\n\n{pin['next']}")