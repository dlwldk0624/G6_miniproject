from pathlib import Path
import random

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="어휘로운 생활",
    page_icon="📚",
    layout="centered",
)

DATA_PATH = Path(__file__).parent / "vocabulary.csv"

REQUIRED_COLUMNS = [
    "No.",
    "Word",
    "Level",
    "Korean meaning (뜻)",
    "Variation",
    "Star mark",
    "Original entry",
    "PDF page",
]


@st.cache_data
def load_data(path):
    try:
        data = pd.read_csv(path, encoding="utf-8-sig")
    except UnicodeDecodeError:
        data = pd.read_csv(path, encoding="cp949")

    missing = [c for c in REQUIRED_COLUMNS if c not in data.columns]
    if missing:
        raise ValueError("Missing columns: " + ", ".join(missing))

    data = data.copy()
    data["Word"] = data["Word"].astype(str).str.strip()
    data["Level"] = data["Level"].astype(str).str.strip()
    data["Korean meaning (뜻)"] = data["Korean meaning (뜻)"].astype(str).str.strip()
    return data


try:
    vocab = load_data(DATA_PATH)
except Exception as e:
    st.error("vocabulary.csv를 불러오지 못했습니다.")
    st.exception(e)
    st.stop()


total_words = len(vocab)
unique_words = vocab["Word"].nunique()
duplicate_words = total_words - unique_words
level_counts = vocab["Level"].value_counts().to_dict()

expected_levels = {
    "Elementary": 800,
    "MidHigh": 1200,
    "Extended": 1000,
}

full_data_ok = (
    total_words == 3000
    and unique_words == 3000
    and duplicate_words == 0
    and all(level_counts.get(k, 0) == v for k, v in expected_levels.items())
)


def init_state():
    defaults = {
        "review_ids": [],
        "flash_ids": [],
        "flash_pos": 0,
        "flash_show": False,
        "quiz_items": [],
        "quiz_pos": 0,
        "quiz_score": 0,
        "quiz_answered": False,
        "quiz_correct": None,
        "spell_ids": [],
        "spell_pos": 0,
        "spell_score": 0,
        "spell_answered": False,
        "spell_correct": None,
        "review_session": [],
        "review_pos": 0,
        "review_answered": False,
        "review_correct": None,
        "review_options": [],
        "last_level": "All",
    }
    for key, value in defaults.items():
