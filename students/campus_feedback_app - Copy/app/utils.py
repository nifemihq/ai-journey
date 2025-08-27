from __future__ import annotations
import io
from typing import Dict, List

import pandas as pd
import streamlit as st


def kpi_row(total: int, pct_pos: float, pct_neg: float) -> None:
    c1, c2, c3 = st.columns(3)
    c1.metric("Total comments", f"{total}")
    c2.metric("% positive", f"{pct_pos:.0%}")
    c3.metric("% negative", f"{pct_neg:.0%}")


def label_distribution_chart(df: pd.DataFrame) -> None:
    ct = (
        df.groupby(["service", "sent_label"]).size().unstack(fill_value=0)
        .reindex(columns=["negative", "neutral", "positive"], fill_value=0)
    )
    st.bar_chart(ct)


def top_examples(df: pd.DataFrame, n: int = 3) -> Dict[str, pd.DataFrame]:
    pos = df.sort_values("sent_score", ascending=False).head(n)[["service", "comment", "sent_score"]]
    neg = df.sort_values("sent_score", ascending=True).head(n)[["service", "comment", "sent_score"]]
    return {"positive": pos, "negative": neg}


def make_action_plan_txt(mood: str, issues: List[str], actions: List[str]) -> bytes:
    lines = [
        "Campus Feedback — Action Plan\n",
        f"Overall mood: {mood}\n\n",
        "Top issues:\n",
    ]
    for i, it in enumerate(issues, 1):
        lines.append(f"  {i}. {it}\n")
    lines.append("\nNext actions:\n")
    for i, act in enumerate(actions, 1):
        lines.append(f"  {i}. {act}\n")
    return "".join(lines).encode("utf-8")


def download_button_bytes(label: str, data: bytes, file_name: str, mime: str = "text/plain"):
    st.download_button(label=label, data=data, file_name=file_name, mime=mime)