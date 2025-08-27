from __future__ import annotations
import re
from functools import lru_cache
from typing import Dict, List, Tuple

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

try:
      from textblob import TextBlob # optional fallback
      _HAS_TEXTBLOB = True
except Exception:
      _HAS_TEXTBLOB = False
      
SENT_THRESH_POS = 0.05
SENT_THRESH_NEG = -0.05

def normalize_text(s: str) -> str:
      if not isinstance(s, str):
            return ""
      s = s.strip().lower()
      # basic cleanup; keep it simple for kids
      s = re.sub(r"\s+", " ", s)
      return s

@lru_cache(maxsize=1)
def get_vader() -> SentimentIntensityAnalyzer:
      return SentimentIntensityAnalyzer()

def score_sentiment(text: str) -> Tuple[float, str]:
    """Return (score, label) using VADER; fallback to TextBlob if needed."""
    if not isinstance(text, str) or not text.strip():
        return 0.0, "neutral"

    t = normalize_text(text)
    score = 0.0
    try:
        analyzer = get_vader()
        score = analyzer.polarity_scores(t)["compound"]
    except Exception:
        if _HAS_TEXTBLOB:
            try:
                score = float(TextBlob(t).sentiment.polarity)
            except Exception:
                score = 0.0

    # Ensure score is a float in [-1, 1]
    try:
        score = float(score)
    except Exception:
        score = 0.0

    if score >= SENT_THRESH_POS:
        label = "positive"
    elif score <= SENT_THRESH_NEG:
        label = "negative"
    else:
        label = "neutral"
    return score, label

def tag_aspects(text: str, service: str, aspects_map: Dict[str, List[str]]) -> List[str]:
      t = normalize_text(text)
      keys = aspects_map.get(service, [])
      found = []
      for kw in keys:
            if kw in t:
                  found.append(kw)
      return found

def prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
      needed = ["timestamp", "service", "comment"]
      for col in needed:
            if col not in df.columns:
                  raise ValueError(f"Missing required column: {col}")
      # Ensure types
      df = df.copy()
      df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
      df["service"] = df["service"].astype(str).str.lower().str.strip()
      df["comment_clean"] = df["comment"].astype(str).map(normalize_text)
      # Sentiment
      scores_labels = df["comment_clean"].map(score_sentiment)
      df["sent_score"] = scores_labels.map(lambda x: x[0])
      df["sent_label"] = scores_labels.map(lambda x: x[1])
      return df
