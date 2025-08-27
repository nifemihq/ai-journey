import sys, os
sys.path.append(os.path.dirname(os.path.dirname('../')))
from app.analysis import prepare_dataframe, score_sentiment

import pandas as pd
from app.analysis import prepare_dataframe, score_sentiment

sample = pd.DataFrame({
    "timestamp": ["2025-08-26"],
    "service": ["library"],
    "comment": ["Quiet and enough seats"],
})

df = prepare_dataframe(sample)
assert "sent_label" in df.columns and len(df) == 1
score, label = score_sentiment("Great food but long queue")
assert -1.0 <= score <= 1.0 and label in {"negative", "neutral", "positive"}
print("OK")