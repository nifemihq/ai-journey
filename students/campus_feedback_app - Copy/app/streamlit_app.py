from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, List

import pandas as pd
import streamlit as st
import yaml

from analysis import prepare_dataframe, tag_aspects
from utils import kpi_row, label_distribution_chart, top_examples, make_action_plan_txt, download_button_bytes

# ---------- Page setup ----------
st.set_page_config(page_title="Campus Service Feedback", page_icon="📊", layout="wide")
st.title("📊 Campus Service Feedback Dashboard")
st.caption("No names stored. Data stays local unless you click Download.")

# ---------- Load aspects config ----------
ASPECTS_PATH = Path(__file__).resolve().parents[1] / "config" / "aspects.yaml"
with open(ASPECTS_PATH, "r", encoding="utf-8") as f:
    ASPECTS = yaml.safe_load(f)

# ---------- Sidebar controls ----------
st.sidebar.header("Controls")
use_sample = st.sidebar.button("Use sample data")
file = st.sidebar.file_uploader("Upload CSV", type=["csv"])  # requires columns: timestamp, service, comment
services = list(ASPECTS.keys())
sel_services = st.sidebar.multiselect("Filter services", services, default=services)
use_openai = st.sidebar.toggle("Use OpenAI for 3-bullet action plan (optional)")

# API key from secrets (do not hardcode)
client = None
if use_openai:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])  # set this in .streamlit/secrets.toml
    except Exception as e:
        st.sidebar.warning("OpenAI client not configured. Check .streamlit/secrets.toml")

# ---------- Load data ----------
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "sample_data.csv"

if use_sample:
    df_raw = pd.read_csv(DATA_PATH)
elif file is not None:
    df_raw = pd.read_csv(file)
else:
    st.info("Upload a CSV or click 'Use sample data' to begin.")
    st.stop()

# Validate and prepare
try:
    df = prepare_dataframe(df_raw)
except Exception as e:
    st.error(f"Data error: {e}")
    st.stop()

# Filter
if sel_services:
    df = df[df["service"].isin([s.lower() for s in sel_services])]

# Aspect tagging
df["aspects"] = df.apply(lambda r: tag_aspects(r["comment"], r["service"], ASPECTS), axis=1)

# KPIs
total = len(df)
pct_pos = (df["sent_label"].eq("positive").mean()) if total else 0
pct_neg = (df["sent_label"].eq("negative").mean()) if total else 0
kpi_row(total, pct_pos, pct_neg)

# Charts
st.subheader("Sentiment by service")
label_distribution_chart(df)

# Examples
st.subheader("Examples")
examples = top_examples(df, n=3)
col1, col2 = st.columns(2)
with col1:
    st.markdown("**Top Positive**")
    st.dataframe(examples["positive"], use_container_width=True)
with col2:
    st.markdown("**Top Negative**")
    st.dataframe(examples["negative"], use_container_width=True)

# Aspect counts
st.subheader("Aspect counts")
aspect_counts = (
    df.explode("aspects").dropna(subset=["aspects"]).groupby(["service", "aspects"]).size().reset_index(name="count")
)
st.dataframe(aspect_counts, use_container_width=True)

# ---------- Optional OpenAI 3-bullet plan ----------
# action_plan = None
# if use_openai and client is not None and len(df) > 0:
#     st.subheader("Action plan (OpenAI)")
#     # Use top 5 negatives and overall label distribution
#     worst = df.sort_values("sent_score").head(5)["comment"].tolist()
#     label_counts = df["sent_label"].value_counts().to_dict()
#     # Prepare a strict JSON instruction for safe parsing
#     system_msg = (
#         "You are a concise campus operations assistant. Return STRICT JSON with keys: "
#         "mood (one of: positive, mixed, negative), top_issues (array of 3 short strings), next_actions (array of 3 short strings). "
#         "Keep each string under 12 words. No extra text."
#     )
#     user_msg = {
#         "worst_examples": worst,
#         "label_counts": label_counts,
#         "aspect_counts": aspect_counts.to_dict(orient="records"),
#     }
#     try:
#         resp = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "system", "content": system_msg},
#                 {"role": "user", "content": json.dumps(user_msg) },
#             ],
#             temperature=0.2,
#         )
#         content = resp.choices[0].message.content
#         parsed = json.loads(content)
#         mood = parsed.get("mood", "mixed")
#         top_issues = parsed.get("top_issues", [])[:3]
#         next_actions = parsed.get("next_actions", [])[:3]
#         st.markdown(f"**Overall mood:** `{mood}`")
#         st.markdown("**Top issues:**")
#         for t in top_issues:
#             st.write("- ", t)
#         st.markdown("**Next actions:**")
#         for a in next_actions:
#             st.write("- ", a)
#         action_plan = (mood, top_issues, next_actions)
#     except Exception as e:
#         st.warning(f"OpenAI summary failed: {e}")

st.subheader("Action plan (Offline)")
if len(df) > 0:
      # Use top 5 negative comments
      worst = df.sort_values("sent_score").head(5)
      # Count most common aspects in those comments
      aspect_counts = worst.explode("aspects")["aspects"].value_counts().head(3)
      top_issues = aspect_counts.index.tolist()


      # Define overall mood simply
      mood = "negative" if pct_neg > 0.4 else ("positive" if pct_pos > 0.5 else "mixed")


      # Next actions = generic fixes per issue
      next_actions = [f"Improve {issue}" for issue in top_issues]


      st.markdown(f"**Overall mood:** `{mood}`")
      st.markdown("**Top issues:**")
      for t in top_issues:
            st.write("- ", t)
      st.markdown("**Next actions:**")
      for a in next_actions:
            st.write("- ", a)

      # Enable download
      from utils import make_action_plan_txt, download_button_bytes
      data = make_action_plan_txt(mood, top_issues, next_actions)
      download_button_bytes("Download action plan (.txt)", data, "action_plan.txt")

# ---------- Downloads ----------
st.subheader("Downloads")
st.download_button(
    label="Download cleaned CSV",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="feedback_cleaned.csv",
    mime="text/csv",
)

# if action_plan:
#     mood, issues, actions = action_plan
#     data = make_action_plan_txt(mood, issues, actions)
#     download_button_bytes("Download action plan (.txt)", data, "action_plan.txt")

# ---------- Footer ----------
st.caption("Educational prototype. Sentiment labels are heuristic and may be imperfect.")