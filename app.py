import streamlit as st
import pandas as pd
import google.generativeai as genai
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import re
from google.api_core.exceptions import ResourceExhausted
from plotly.graph_objs._figure import Figure as PlotlyFigure

# =========================================================
# CONFIG
# =========================================================
AI_MODE = "ONLINE"   # "ONLINE" or "OFFLINE"
GEMINI_MODEL = "models/gemini-2.5-flash-lite"

st.set_page_config(page_title="InsightStream", layout="wide")
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# =========================================================
# PROMPT-INJECTION DEFENSE
# =========================================================
INJECTION_PATTERNS = [
    r"ignore .* instruction",
    r"disregard .* rules",
    r"system prompt",
    r"import\s+",
    r"exec\(",
    r"eval\(",
    r"subprocess",
    r"open\(",
    r"__",
    r"pip install",
]

def is_prompt_injection(query: str) -> bool:
    q = query.lower()
    return any(re.search(p, q) for p in INJECTION_PATTERNS)

# =========================================================
# GEMINI CALL
# =========================================================
def ask_gemini(prompt: str) -> str:
    model = genai.GenerativeModel(GEMINI_MODEL)
    response = model.generate_content(prompt)
    if not response or not response.text:
        raise RuntimeError("Empty Gemini response")
    return response.text.strip()

# =========================================================
# SANITIZE GENERATED CODE
# =========================================================
def sanitize_generated_code(code: str, columns: list[str]) -> str:
    for col in columns:
        code = re.sub(rf"df\[\s*{col}\s*\]", f"df['{col}']", code)
    code = re.sub(r"df\[(?!['\"])([^\]]+)\]", r"df['\1']", code)
    return code

# =========================================================
# AI CORE
# =========================================================
def analyze_with_ai(df: pd.DataFrame, user_query: str) -> dict:
    if AI_MODE == "OFFLINE":
        return {"status": "AI_OFFLINE"}

    columns = df.columns.tolist()
    col_str = ", ".join(columns)

    prompt = f"""
You are a STRICT JSON API. Output ONLY valid JSON.

Dataset columns:
{col_str}

User question:
"{user_query}"

TASK:
1. Decide VALID or INVALID
2. If INVALID → explain why
3. If VALID:
   - Generate EXECUTABLE Python code
   - Generate 2–4 short business insights

CODE RULES:
- DataFrame name is df
- Use ONLY: df, pd, px, go, make_subplots
- NEVER invent column names
- ALWAYS wrap column names in quotes
- Do NOT import
- Do NOT print
- Output MUST define EXACTLY ONE: fig or result_df

SECURITY:
- Do NOT modify system behavior
- Do NOT access files/env
- Do NOT explain concepts

JSON FORMAT:
{{
  "status": "VALID or INVALID",
  "reason": "...",
  "code": "python code or null",
  "insights": ["...", "..."] or null
}}
"""
    try:
        raw = ask_gemini(prompt)
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not match:
            raise ValueError("No JSON found")

        data = json.loads(match.group())
        if data.get("code"):
            data["code"] = sanitize_generated_code(data["code"], columns)
        return data

    except ResourceExhausted:
        return {"status": "AI_OFFLINE"}
    except Exception:
        return {
            "status": "INVALID",
            "reason": "AI response could not be parsed safely.",
            "code": None,
            "insights": None
        }

# =========================================================
# SAFE EXECUTION
# =========================================================
def execute_analysis_code(code: str, df: pd.DataFrame):
    safe_env = {
        "df": df.copy(),
        "pd": pd,
        "px": px,
        "go": go,
        "make_subplots": make_subplots
    }
    try:
        exec(code, {}, safe_env)
    except Exception as e:
        return None, f"Execution error: {e}"

    fig = safe_env.get("fig")
    if isinstance(fig, PlotlyFigure):
        return fig, None

    result_df = safe_env.get("result_df")
    if isinstance(result_df, pd.DataFrame):
        return result_df, None

    return None, "No valid output produced"

# =========================================================
# OFFLINE FALLBACK
# =========================================================
def run_offline_analysis(df: pd.DataFrame):
    st.subheader("📉 Offline Analytics Mode")
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if not numeric_cols:
        st.info("No numeric columns available for analysis.")
        return

    # Correlation matrix
    corr = df[numeric_cols].corr()
    fig = px.imshow(corr, text_auto=True, title="Correlation Matrix")
    st.plotly_chart(fig, use_container_width=True)

    # Try trend plots for numeric columns with time columns
    time_cols = df.select_dtypes(include=["datetime", "object"]).columns.tolist()
    for col in time_cols:
        try:
            temp = df.copy()
            temp[col] = pd.to_datetime(temp[col], errors="coerce")
            if temp[col].isna().all():
                continue
            for num in numeric_cols:
                trend = temp.groupby(temp[col].dt.to_period("M"))[num].mean().reset_index()
                trend[col] = trend[col].astype(str)
                fig = px.line(trend, x=col, y=num, title=f"{num} Trend Over Time")
                st.plotly_chart(fig, use_container_width=True)
            break
        except Exception:
            continue

# =========================================================
# UI
# =========================================================
st.title("📊 InsightStream")
st.subheader("AI That Prevents Misleading Data Insights")

if AI_MODE == "ONLINE":
    st.success("🟢 AI Online Mode (Gemini)")
else:
    st.info("🟡 Offline Mode (Rule-Based)")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("Dataset loaded")
    st.dataframe(df.head())

    user_query = st.text_area(
        "Ask a question",
        placeholder="Example: Show monthly sales trend over time"
    )

    if st.button("Analyze"):
        if not user_query.strip():
            st.warning("Enter a question")
            st.stop()

        if is_prompt_injection(user_query):
            st.error("🚫 Unsafe query detected")
            st.stop()

        with st.spinner("Analyzing..."):
            result = analyze_with_ai(df, user_query)

        if result["status"] == "AI_OFFLINE":
            st.warning("⚠️ AI unavailable → Offline analytics")
            run_offline_analysis(df)
            st.stop()

        if result["status"] == "INVALID":
            st.error("❌ Invalid question")
            st.write(result["reason"])
            st.stop()

        st.success("✅ Question validated")

        output, error = execute_analysis_code(result["code"], df)

        if error:
            st.error("❌ Analysis failed")
            st.code(result["code"], language="python")
            st.write(error)
            st.stop()

        if isinstance(output, pd.DataFrame):
            st.dataframe(output)
        elif isinstance(output, PlotlyFigure):
            st.plotly_chart(output, use_container_width=True)
        else:
            st.warning("Output generated but could not be rendered.")

        if result.get("insights"):
            st.markdown("### 🧠 Key Insights")
            for insight in result["insights"]:
                st.write("•", insight)

        with st.expander("🔍 View Generated Code"):
            st.code(result["code"], language="python")
