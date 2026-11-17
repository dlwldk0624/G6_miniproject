from pathlib import Path
import random
import pandas as pd
import streamlit as st

st.set_page_config(page_title="어휘로운 생활", page_icon="📚")

@st.cache_data
def load_vocab():
    path = Path(__file__).parent / "vocabulary.csv"
    try:
        df = pd.read_csv(path, encoding="utf-8-sig")
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding="cp949")
    df["Word"] = df["Word"].astype(str).str.strip()
    df["Level"] = df["Level"].astype(str).str.strip()
    df["Korean meaning (뜻)"] = df["Korean meaning (뜻)"].astype(str).str.strip()
    return df

df = load_vocab()
st.title("📚 어휘로운 생활")
st.caption("G6 Vocabulary Learning App")

if len(df) == 3000 and df["Word"].nunique() == 3000:
    st.success("✅ Vocabulary loaded: 3,000 words")
else:
    st.error(f"데이터 확인 필요: {len(df)} rows / {df['Word'].nunique()} unique")

level = st.sidebar.selectbox("학습 수준", ["All", "Elementary", "MidHigh", "Extended"])
pool = df if level == "All" else df[df["Level"] == level]
st.sidebar.write(f"현재 학습 풀: {len(pool):,} words")

for key, value in {"review": [], "flash": None, "quiz": None, "spell": None}.items():
    if key not in st.session_state:
        st.session_state[key] = value

tab1, tab2, tab3, tab4 = st.tabs(["🃏 Flashcards", "📖 Meaning Quiz", "✏️ Spelling", "🔁 Review"])

with tab1:
    st.subheader("Flashcards")
    if st.button("새 카드 뽑기"):
        st.session_state.flash = pool.sample(1).iloc[0].to_dict()
    if st.session_state.flash:
        r = st.session_state.flash
        st.markdown(f"## {r['Word']}")
        with st.expander("뜻 보기"):
            st.write(r["Korean meaning (뜻)"])
            st.caption(f"Level: {r['Level']}")

with tab2:
    st.subheader("Meaning Quiz")
    if st.button("새 뜻 퀴즈"):
        r = pool.sample(1).iloc[0]
        wrongs = pool[pool["Korean meaning (뜻)"] != r["Korean meaning (뜻)"]].sample(3)
        opts = wrongs["Korean meaning (뜻)"].tolist() + [r["Korean meaning (뜻)"]]
        random.shuffle(opts)
        st.session_state.quiz = {"no": int(r["No."]), "word": r["Word"], "answer": r["Korean meaning (뜻)"], "opts": opts}
    if st.session_state.quiz:
        q = st.session_state.quiz
        choice = st.radio(q["word"], q["opts"], index=None, key="quiz_choice")
        if st.button("뜻 정답 확인") and choice:
            if choice == q["answer"]:
                st.success("✅ 정답!")
            else:
                st.error(f"❌ 정답: {q['answer']}")
                if q["no"] not in st.session_state.review:
                    st.session_state.review.append(q["no"])

with tab3:
    st.subheader("Spelling Practice")
    if st.button("새 철자 문제"):
        r = pool.sample(1).iloc[0]
        st.session_state.spell = {"no": int(r["No."]), "word": r["Word"], "meaning": r["Korean meaning (뜻)"]}
    if st.session_state.spell:
        q = st.session_state.spell
        st.write(f"뜻: **{q['meaning']}**")
        answer = st.text_input("영어 단어 입력", key="spell_input")
        if st.button("철자 정답 확인") and answer:
            if answer.strip().lower() == q["word"].lower():
                st.success("✅ 정답!")
            else:
                st.error(f"❌ 정답: {q['word']}")
                if q["no"] not in st.session_state.review:
                    st.session_state.review.append(q["no"])

with tab4:
    st.subheader("Review Again")
    if not st.session_state.review:
        st.success("복습할 단어가 없어요.")
    else:
        review_df = df[df["No."].isin(st.session_state.review)][["Word", "Korean meaning (뜻)", "Level"]]
        st.dataframe(review_df, use_container_width=True, hide_index=True)
        if st.button("복습 목록 비우기"):
            st.session_state.review = []
            st.rerun()
