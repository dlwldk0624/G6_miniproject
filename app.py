from pathlib import Path
from io import BytesIO
import random

import pandas as pd
import streamlit as st
from gtts import gTTS


st.set_page_config(
    page_title="어휘로운 생활",
    page_icon="📚",
    layout="centered",
)

CSS = (
    "<style>"
    ".block-container{max-width:950px;padding-top:2rem;padding-bottom:4rem;}"
    "html,body,[class*='css']{font-size:19px;}"
    "h1{font-size:3rem!important;font-weight:900!important;}"
    "h2{font-size:2.1rem!important;font-weight:900!important;}"
    "h3{font-size:1.6rem!important;font-weight:800!important;}"
    "p,div,label{font-size:1.1rem;}"
    ".stButton>button{min-height:62px;font-size:1.12rem;font-weight:800;border-radius:15px;padding:.8rem 1.3rem;}"
    ".stTextInput input{min-height:62px;font-size:1.3rem!important;border-radius:15px;padding:.75rem 1rem;}"
    ".stSelectbox div[data-baseweb='select']>div{min-height:58px;font-size:1.08rem;}"
    ".stRadio label{font-size:1.1rem!important;padding:.35rem 0;}"
    "div[data-testid='stMetricValue']{font-size:2.1rem;}"
    "div[data-testid='stAlert']{font-size:1.08rem;}"
    ".word-card{border:3px solid #4c63ff;border-radius:24px;padding:40px 22px;text-align:center;background:#fbfcff;margin:20px 0;}"
    ".word-main{font-size:3.5rem;font-weight:900;color:#4056e8;line-height:1.15;letter-spacing:-.02em;}"
    ".word-meaning{font-size:2rem;font-weight:900;margin-top:14px;line-height:1.35;}"
    ".word-meta{font-size:1.05rem;color:#68708a;margin-top:16px;line-height:1.75;}"
    ".big-note{font-size:1.2rem!important;font-weight:700;color:#68708a;line-height:1.65;}"
    "@media(max-width:640px){"
    ".block-container{padding-left:1rem;padding-right:1rem;padding-top:1rem;}"
    "html,body,[class*='css']{font-size:18px;}"
    "h1{font-size:2.35rem!important;}"
    "h2{font-size:1.8rem!important;}"
    ".word-card{padding:32px 16px;}"
    ".word-main{font-size:2.85rem;}"
    ".word-meaning{font-size:1.65rem;}"
    ".stButton>button{min-height:62px;font-size:1.08rem;}"
    ".stTextInput input{min-height:62px;font-size:1.2rem!important;}"
    "}"
    "</style>"
)

st.markdown(CSS, unsafe_allow_html=True)


DATA_PATH = Path(__file__).resolve().parent / "vocabulary.csv"


@st.cache_data
def load_vocab():
    if not DATA_PATH.exists():
        st.error("❌ vocabulary.csv 파일을 찾지 못했습니다.")
        st.caption("app.py와 vocabulary.csv를 GitHub 저장소의 같은 폴더에 두어 주세요.")
        st.stop()

    try:
        data = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
    except UnicodeDecodeError:
        data = pd.read_csv(DATA_PATH, encoding="cp949")

    required = ["No.", "Word", "Level", "Korean meaning (뜻)"]
    missing = [column for column in required if column not in data.columns]

    if missing:
        st.error("❌ CSV에 필요한 열이 없습니다: " + ", ".join(missing))
        st.stop()

    data = data.copy()
    data["Word"] = data["Word"].astype(str).str.strip()
    data["Level"] = data["Level"].astype(str).str.strip()
    data["Korean meaning (뜻)"] = data["Korean meaning (뜻)"].astype(str).str.strip()
    return data


@st.cache_data(show_spinner=False)
def make_tts(word):
    audio_buffer = BytesIO()
    voice = gTTS(text=word, lang="en", tld="com")
    voice.write_to_fp(audio_buffer)
    return audio_buffer.getvalue()


df = load_vocab()

total_words = len(df)
unique_words = df["Word"].nunique()
level_counts = df["Level"].value_counts().to_dict()

st.title("📚 어휘로운 생활")
st.caption("G6 Vocabulary Learning App · Streamlit Version")
