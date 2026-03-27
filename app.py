import streamlit as st
import plotly.express as px
import pandas as pd

from db import load_data, run_query, get_schema
from ai import nl_to_sql, verify_trust, generate_insight

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Co-Pilot",
    page_icon="🚀",
    layout="wide"
)

# ── Hide default Streamlit footer ─────────────────────────────────────────────
# st.markdown("""
#     <style>
#         #MainMenu {visibility: hidden;}
#         footer {visibility: hidden;}
#         /* header {visibility: hidden;} */
#         .block-container { padding-top: 1.5rem; }
#     </style>
# """, unsafe_allow_html=True)

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

# ── Helpers ───────────────────────────────────────────────────────────────────
def show_confidence(confidence: str, reason: str):
    if confidence == "high":
        st.success(f"✅ Confidence: High — {reason}")
    elif confidence == "medium":
        st.warning(f"⚠️ Confidence: Medium — {reason}")
    else:
        st.error(f"🔴 Confidence: Low — {reason}")

def build_summary(result_df: pd.DataFrame) -> str:
    return (
        f"{len(result_df)} rows returned. "
        f"Columns: {list(result_df.columns)}. "
        f"Sample: {result_df.head(2).to_dict()}"
    )

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
        fig = px.line(result_df, x=num_cols[0], y=num_cols[1], title=title)
        st.plotly_chart(fig, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════════
# HEADER — BCG Logo + Title
# ════════════════════════════════════════════════════════════════════════════════
logo_col, title_col = st.columns([1, 6])

with logo_col:
    st.markdown("""
        <div style="padding-top: 6px;">
            <svg width="68" height="68" viewBox="0 0 68 68"
                 xmlns="http://www.w3.org/2000/svg">
                <rect width="68" height="68" rx="6" fill="#00A850"/>
                <text x="34" y="44" text-anchor="middle"
                      font-family="Arial, sans-serif"
                      font-size="21" font-weight="bold"
                      fill="white" letter-spacing="1">BCG</text>
            </svg>
        </div>
    """, unsafe_allow_html=True)

with title_col:
    st.title("AI-Powered Executive Data & BI Co-Pilot")
    st.markdown(
        "Interact with your business data seamlessly<br>"
        "<small style='opacity:0.55;'>Note: Running on the Gemini API free tier; "
        "rate limits may be encountered.</small>",
        unsafe_allow_html=True
    )

st.divider()



# ════════════════════════════════════════════════════════════════════════════════
# SECTION 1 — Ask Anything (top, right after header)
# ════════════════════════════════════════════════════════════════════════════════
st.subheader("Intelligent AI Insights Assistant")

question = st.text_input(
    "Use natural language to analyze data, discover trends, and generate insights",
    placeholder="e.g. Which region had the highest profit last year?",
    key="question_input"
)

ask_clicked = st.button("Ask", type="primary")

if ask_clicked and question.strip():
    with st.spinner("Thinking..."):

        sql_result = nl_to_sql(question, schema)

        if "error" in sql_result:
            st.error(f"Could not generate SQL: {sql_result['error']}")
        else:
            sql = sql_result.get("sql", "")
            assumptions = sql_result.get("assumptions", [])
            result = run_query(conn, sql)

            if isinstance(result, str):
                st.error(f"Query failed: {result}")
                with st.expander("See SQL that failed"):
                    st.code(sql, language="sql")

            elif isinstance(result, pd.DataFrame):
                summary = build_summary(result)
                trust = verify_trust(question, sql, summary)

                confidence = trust.get("confidence", "medium")
                reason = trust.get("reason", "")
                flags = trust.get("flags", [])

                show_confidence(confidence, reason)

                if assumptions:
                    st.info("💡 Assumptions made: " + " · ".join(assumptions))

                if flags:
                    st.warning("⚠️ Data flags: " + " · ".join(flags))

                st.dataframe(result, use_container_width=True)
                auto_chart(result, title=question)

                with st.expander("🔍 See SQL query"):
                    st.code(sql, language="sql")

                st.session_state["current"] = {
                    "question": question,
                    "sql": sql,
                    "result": result,
                    "summary": summary,
                    "confidence": confidence,
                    "reason": reason,
                }
                st.session_state["current_insight"] = None


# ── Generate Insight ──────────────────────────────────────────────────────────
if st.session_state["current"]:
    st.divider()

    if st.button("✨ Generate Insight", type="secondary"):
        with st.spinner("Generating insight..."):
            current = st.session_state["current"]
            insight = generate_insight(current["question"], current["summary"])
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
# SECTION 2 — KPI Metric Cards
# ════════════════════════════════════════════════════════════════════════════════
st.divider()

total_sales = df["Sales"].sum()
total_orders = len(df)
avg_margin = (df["Profit"] / df["Sales"]).mean() * 100

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Sales", f"${total_sales/1_000_000:.2f}M")
col2.metric("📦 Total Orders", f"{total_orders:,}")
col3.metric("📈 Avg Profit Margin", f"{avg_margin:.1f}%")

st.markdown("<br>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# SECTION 3 — Two Charts Side by Side (50/50)
# ════════════════════════════════════════════════════════════════════════════════
chart_col1, chart_col2 = st.columns(2)

# ── Chart 1: Sales by Region ──────────────────────────────────────────────────
with chart_col1:
    st.subheader("Sales by Region")
    region_df = (
        df.groupby("Region")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Sales", ascending=False)
    )
    fig_region = px.bar(
        region_df,
        x="Region",
        y="Sales",
        color="Region",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_region.update_layout(
        showlegend=False,
        margin=dict(t=10, b=20),
        yaxis_tickprefix="$",
        yaxis_tickformat=",.0f"
    )
    st.plotly_chart(fig_region, use_container_width=True)

# ── Chart 2: Top 10 Products by Sales ────────────────────────────────────────
with chart_col2:
    st.subheader("Top 10 Products by Sales")

    product_col = None
    for col in df.columns:
        if "product" in col.lower() and "name" in col.lower():
            product_col = col
            break
    if product_col is None:
        for col in df.columns:
            if "product" in col.lower():
                product_col = col
                break

    if product_col:
        top_products = (
            df.groupby(product_col)["Sales"]
            .sum()
            .reset_index()
            .sort_values("Sales", ascending=False)
            .head(10)
        )
        fig_products = px.bar(
            top_products,
            x="Sales",
            y=product_col,
            orientation="h",
            color="Sales",
            color_continuous_scale="Teal"
        )
        fig_products.update_layout(
            margin=dict(t=10, b=20),
            yaxis=dict(autorange="reversed"),
            coloraxis_showscale=False,
            xaxis_tickprefix="$",
            xaxis_tickformat=",.0f"
        )
        st.plotly_chart(fig_products, use_container_width=True)
    else:
        cat_df = df.groupby("Category")["Sales"].sum().reset_index()
        fig_cat = px.pie(
            cat_df,
            values="Sales",
            names="Category",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_cat.update_layout(margin=dict(t=10, b=20))
        st.plotly_chart(fig_cat, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════════
# SECTION 4 — Pin & Saved Insights
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
    for pin in reversed(st.session_state["pinned"]):
        with st.expander(f"❓ {pin['question']}"):
            show_confidence(pin["confidence"], pin["reason"])
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info(f"**What happened**\n\n{pin['what']}")
            with col2:
                st.info(f"**Why**\n\n{pin['why']}")
            with col3:
                st.info(f"**Recommended action**\n\n{pin['next']}")


# # ════════════════════════════════════════════════════════════════════════════════
# # FOOTER
# # ════════════════════════════════════════════════════════════════════════════════


st.markdown("""
    <div style="text-align: center; padding: 10px 0 28px 0;
                font-size: 14px; opacity: 0.65;">
        Developed by <strong>Pavel Bodle</strong> &nbsp;|&nbsp;
        <a href="https://www.linkedin.com/in/pavelbodle/"
           target="_blank"
           style="color: #0A66C2; text-decoration: none; font-weight: 600;">
            LinkedIn (Connect with me)
        </a>
        &nbsp;|&nbsp;
        <a href="https://github.com/PavelBodle"
           target="_blank"
           style="color: #333; text-decoration: none; font-weight: 600;">
            GitHub (Source Code)
        </a>

    </div>
""", unsafe_allow_html=True)
