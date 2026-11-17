from pathlib import Path
import random

import pandas as pd
import streamlit as st


# =========================================================
# PAGE SETUP
# =========================================================

st.set_page_config(
    page_title="어휘로운 생활",
    page_icon="📚",
    layout="centered",
)

st.markdown(
    """
    <style>
    .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    .app-title {
        font-size: 2.2rem;
        font-weight: 900;
        color: #1f43c7;
        margin-bottom: 0.2rem;
    }

    .app-subtitle {
        color: #5b6785;
        margin-bottom: 1rem;
    }

    .word-card {
        border: 2px solid #d9e1f5;
        border-radius: 18px;
        padding: 28px 24px;
        text-align: center;
        background: #ffffff;
        margin: 12px 0 18px 0;
    }

    .word-main {
        font-size: 2.6rem;
        font-weight: 900;
        color: #2d5bff;
        margin-bottom: 0.5rem;
    }

    .word-meaning {
        font-size: 1.6rem;
        font-weight: 800;
        color: #1b2540;
        margin-bottom: 0.7rem;
    }

    .small-note {
        color: #5b6785;
        font-size: 0.9rem;
    }

    .data-ok {
        padding: 12px 14px;
        background: #e0f6ee;
        color: #07694d;
        border-radius: 12px;
        font-weight: 800;
        margin-bottom: 14px;
    }

    .data-warn {
        padding: 12px 14px;
        background: #fde8e7;
        color: #9a2623;
        border-radius: 12px;
        font-weight: 800;
        margin-bottom: 14px;
    }

    .review-card {
        background: #f5f7ff;
        border: 1px solid #d9e1f5;
        border-radius: 14px;
        padding: 12px 14px;
        margin: 7px 0;
    }

    @media (max-width: 600px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
