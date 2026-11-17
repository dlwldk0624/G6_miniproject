from pathlib import Path
from io import BytesIO
import random
import pandas as pd
import streamlit as st
from gtts import gTTS

st.set_page_config(
    page_title="어휘로운 생활",
    page_icon="📚",
    layout="centered"
)

st.markdown("""
<style>
.block-container{
    max-width:950px;
    padding-top:2rem;
    padding-bottom:4rem;
}

h1{
    font-size:3rem!important;
    font-weight:900!important;
}

h2{
    font-size:2rem!important;
    font-weight:900!important;
}

p,label,div{
    font-size:1.08rem;
}

.word-card{
    border:3px solid #4c63ff;
    border-radius:24px;
    background:#f9faff;
    padding:40px 22px;
    margin:20px 0;
    text-align:center;
}

.word{
    font-size:3.5rem;
    font-weight:900;
    color:#4056e8;
    line-height:1.15;
}

.meaning{
    font-size:2rem;
    font-weight:900;
    margin-top:14px;
}

.stButton>button,
.stFormSubmitButton>button{
    min-height:60px;
    font-size:1.08rem;
    font-weight:800;
    border-radius:14px;
}

.stTextInput input{
    min-height:60px;
    font-size:1.25rem!important;
    border-radius:14px;
}

@media(max-width:640px){
    .block-container{
        padding:1rem;
    }

    h1{
        font-size:2.3rem!important;
    }

    h2{
        font-size:1.7rem!important;
    }

    .word-card{
        padding:30px 16px;
    }

    .word{
        font-size:2.8rem;
    }

    .meaning{
        font-size:1.6rem;
    }
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_vocab():

    base = Path(__file__).resolve().parent

    candidates = [
        base / "vocabulary.csv",
        base / "Voca_3000.csv",
        base / "Voca_3000(1).csv",
    ]

    path = next(
        (p for p in candidates if p.exists()),
        None
    )

    if path is None:
        csvs = list(base.glob("*.csv"))

        if len(csvs) == 1:
            path = csvs[0]

    if path is None:
        st.error("❌ CSV 파일을 찾지 못했습니다.")
        st.write(
            "app.py와 vocabulary.csv를 "
            "GitHub의 같은 폴더에 올려 주세요."
        )
        st.stop()

    try:
        df = pd.read_csv(
            path,
            encoding="utf-8-sig"
        )

    except UnicodeDecodeError:
        df = pd.read_csv(
            path,
            encoding="cp949"
        )

    required = [
        "No.",
        "Word",
        "Level",
        "Korean meaning (뜻)"
    ]

    missing = [
        c
        for c in required
        if c not in df.columns
    ]

    if missing:

        st.error(
            "❌ CSV에 필요한 열이 없습니다: "
            + ", ".join(missing)
        )

        st.stop()

    df = df.copy()

    df["Word"] = (
        df["Word"]
        .astype(str)
        .str.strip()
    )

    df["Level"] = (
        df["Level"]
        .astype(str)
        .str.strip()
    )

    df["Korean meaning (뜻)"] = (
        df["Korean meaning (뜻)"]
        .astype(str)
        .str.strip()
    )

    return df, path.name


@st.cache_data(show_spinner=False)
def make_tts(word):

    audio = BytesIO()

    gTTS(
        text=word,
        lang="en",
        tld="com"
    ).write_to_fp(audio)

    return audio.getvalue()


df, csv_name = load_vocab()


defaults = {
    "flash": None,
    "quiz": None,
    "quiz_feedback": None,
    "spell": None,
    "spell_feedback": None,
    "review": [],
    "last_level": "All",
}


for k, v in defaults.items():

    if k not in st.session_state:
        st.session_state[k] = v


def random_row(pool, previous_no=None):

    choices = pool

    if previous_no is not None and len(pool) > 1:

        choices = pool[
            pool["No."] != int(previous_no)
        ]

    return choices.sample(1).iloc[0]


def add_review(no_value):

    no_value = int(no_value)

    if no_value not in st.session_state.review:
        st.session_state.review.append(no_value)


def show_card(word, meaning=None):

    html = (
        "<div class='word-card'>"
        f"<div class='word'>{word}</div>"
    )

    if meaning is not None:

        html += (
            f"<div class='meaning'>"
            f"{meaning}"
            f"</div>"
        )

    html += "</div>"

    st.markdown(
        html,
        unsafe_allow_html=True
    )


def tts_button(word, key):

    if st.button(
        "🔊 발음 듣기",
        key=key,
        use_container_width=True
    ):

        try:

            st.audio(
                make_tts(word),
                format="audio/mp3",
                autoplay=True
            )

        except Exception:

            st.warning(
                "발음을 불러오지 못했어요. "
                "잠시 후 다시 눌러 주세요."
            )


st.title("📚 어휘로운 생활")

st.caption(
    "G6 Vocabulary Learning App · "
    "Streamlit Version"
)


counts = (
    df["Level"]
    .value_counts()
    .to_dict()
)


if (
    len(df) == 3000
    and df["Word"].nunique() == 3000
    and counts.get("Elementary", 0) == 800
    and counts.get("MidHigh", 0) == 1200
    and counts.get("Extended", 0) == 1000
):

    st.success(
        "✅ 3,000 words loaded "
        "· Elementary 800 "
        "· MidHigh 1,200 "
        "· Extended 1,000"
    )

else:

    st.warning(
        f"⚠️ 데이터 확인 필요: "
        f"{len(df)} rows / "
        f"{df['Word'].nunique()} unique words"
    )


with st.sidebar:

    st.header("⚙️ 학습 설정")

    level = st.selectbox(
        "학습 수준",
        [
            "All",
            "Elementary",
            "MidHigh",
            "Extended"
        ]
    )

    if level == "All":

        pool = df

    else:

        pool = df[
            df["Level"] == level
        ]

    st.metric(
        "현재 학습 풀",
        f"{len(pool):,} words"
    )

    st.caption(
        f"사용 중인 CSV: {csv_name}"
    )

    st.write(
        "복습 대기:",
        f"**{len(st.session_state.review)}개**"
    )


if level != st.session_state.last_level:

    st.session_state.last_level = level

    st.session_state.flash = None
    st.session_state.quiz = None
    st.session_state.quiz_feedback = None
    st.session_state.spell = None
    st.session_state.spell_feedback = None


tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🃏 Flashcards",
        "📖 Meaning Quiz",
        "✏️ Spelling Practice",
        "🔁 Review Again"
    ]
)


# =========================================================
# FLASHCARDS
# =========================================================

with tab1:

    st.subheader("🃏 Flashcards")

    st.write(
        "영어 단어를 보고 뜻을 떠올린 뒤 "
        "발음과 뜻을 확인하세요."
    )

    if st.button(
        "🎲 새 단어 뽑기",
        key="new_flash",
        use_container_width=True
    ):

        if st.session_state.flash:

            prev = (
                st.session_state.flash["No."]
            )

        else:

            prev = None

        st.session_state.flash = (
            random_row(
                pool,
                prev
            ).to_dict()
        )


    if st.session_state.flash is None:

        st.info(
            "새 단어 뽑기를 눌러 "
            "학습을 시작하세요."
        )

    else:

        row = st.session_state.flash

        show_card(
            row["Word"]
        )

        tts_button(
            row["Word"],
            "flash_tts_"
            + str(row["No."])
        )

        with st.expander(
            "💡 뜻과 정보 보기"
        ):

            st.markdown(
                "### "
                + str(
                    row[
                        "Korean meaning (뜻)"
                    ]
                )
            )

            st.write(
                "**Level:**",
                row["Level"]
            )

            variation = row.get(
                "Variation",
                ""
            )

            if (
                pd.notna(variation)
                and str(variation).strip()
            ):

                st.write(
                    "**관련어 / Variation:**",
                    variation
                )


# =========================================================
# MEANING QUIZ
# =========================================================

with tab2:

    st.subheader(
        "📖 Meaning Quiz"
    )

    st.write(
        "영어 단어를 보고 "
        "알맞은 한국어 뜻을 고르세요."
    )


    if st.button(
        "🎲 새 뜻 퀴즈",
        key="new_quiz",
        use_container_width=True
    ):

        if st.session_state.quiz:

            prev = (
                st.session_state.quiz["no"]
            )

        else:

            prev = None

        row = random_row(
            pool,
            prev
        )

        correct = (
            row["Korean meaning (뜻)"]
        )

        distractor_pool = pool[
            pool["Korean meaning (뜻)"]
            != correct
        ].drop_duplicates(
            subset=[
                "Korean meaning (뜻)"
            ]
        )

        if len(distractor_pool) < 3:

            distractor_pool = df[
                df["Korean meaning (뜻)"]
                != correct
            ].drop_duplicates(
                subset=[
                    "Korean meaning (뜻)"
                ]
            )

        distractors = (
            distractor_pool
            .sample(3)[
                "Korean meaning (뜻)"
            ]
            .tolist()
        )

        options = (
            distractors
            + [correct]
        )

        random.shuffle(options)

        st.session_state.quiz = {
            "no": int(row["No."]),
            "word": row["Word"],
            "answer": correct,
            "options": options
        }

        st.session_state.quiz_feedback = None


    if st.session_state.quiz is None:

        st.info(
            "새 뜻 퀴즈를 눌러 "
            "시작하세요."
        )

    else:

        q = st.session_state.quiz

        show_card(
            q["word"]
        )

        tts_button(
            q["word"],
            "quiz_tts_"
            + str(q["no"])
        )

        choice = st.radio(
            "알맞은 뜻을 고르세요.",
            q["options"],
            index=None,
            key=(
                "quiz_choice_"
                + str(q["no"])
            )
        )


        if st.button(
            "정답 확인",
            key=(
                "quiz_check_"
                + str(q["no"])
            ),
            use_container_width=True
        ):

            if choice is None:

                st.warning(
                    "답을 먼저 선택해 주세요."
                )

            elif choice == q["answer"]:

                st.session_state.quiz_feedback = (
                    "ok",
                    "✅ 정답이에요!"
                )

            else:

                add_review(
                    q["no"]
                )

                st.session_state.quiz_feedback = (
                    "bad",
                    "❌ 정답은 '"
                    + q["answer"]
                    + "'예요."
                )


        if st.session_state.quiz_feedback:

            kind, msg = (
                st.session_state.quiz_feedback
            )

            if kind == "ok":

                st.success(msg)

            else:

                st.error(msg)


# =========================================================
# SPELLING PRACTICE
# =========================================================

with tab3:

    st.subheader(
        "✏️ Spelling Practice"
    )

    st.write(
        "한국어 뜻을 보고 영어 단어를 입력하세요. "
        "**Enter를 누르면 채점 후 "
        "바로 다음 문제로 넘어갑니다.**"
    )


    if st.session_state.spell_feedback:

        kind, msg = (
            st.session_state.spell_feedback
        )

        if kind == "ok":

            st.success(msg)

        else:

            st.error(msg)


    if st.session_state.spell is None:

        if st.button(
            "▶️ 철자 학습 시작",
            key="start_spell",
            use_container_width=True
        ):

            row = random_row(pool)

            st.session_state.spell = {
                "no": int(row["No."]),
                "word": row["Word"],
                "meaning": row[
                    "Korean meaning (뜻)"
                ]
            }

            st.session_state.spell_feedback = None

            st.rerun()


        st.info(
            "철자 학습 시작을 눌러 주세요."
        )

    else:

        s = st.session_state.spell

        show_card(
            "?",
            s["meaning"]
        )

        st.caption(
            f"첫 글자: {s['word'][0]} "
            f"· 총 {len(s['word'])}글자"
        )


        with st.form(
            "spelling_form_"
            + str(s["no"]),
            clear_on_submit=True,
            enter_to_submit=True
        ):

            typed = st.text_input(
                "영어 단어 입력",
                placeholder=(
                    "정답을 입력하고 "
                    "Enter를 누르세요"
                ),
                autocomplete="off"
            )

            submitted = (
                st.form_submit_button(
                    "정답 제출",
                    use_container_width=True
                )
            )


        if submitted:

            answer = (
                typed
                .strip()
                .lower()
            )


            if not answer:

                st.warning(
                    "단어를 먼저 입력해 주세요."
                )

            else:

                old_no = s["no"]
                old_word = s["word"]


                if (
                    answer
                    == old_word.lower()
                ):

                    st.session_state.spell_feedback = (
                        "ok",
                        "✅ 정답! "
                        + old_word
                        + " · 다음 문제입니다."
                    )

                else:

                    add_review(
                        old_no
                    )

                    st.session_state.spell_feedback = (
                        "bad",
                        "❌ 정답은 '"
                        + old_word
                        + "'였어요. "
                        + "복습 목록에 저장했습니다."
                    )


                next_row = random_row(
                    pool,
                    old_no
                )


                st.session_state.spell = {
                    "no": int(
                        next_row["No."]
                    ),
                    "word": next_row[
                        "Word"
                    ],
                    "meaning": next_row[
                        "Korean meaning (뜻)"
                    ]
                }

                st.rerun()


# =========================================================
# REVIEW AGAIN
# =========================================================

with tab4:

    st.subheader(
        "🔁 Review Again"
    )

    st.write(
        "Meaning Quiz와 "
        "Spelling Practice에서 "
        "틀린 단어를 다시 확인하세요."
    )


    valid_ids = set(
        df["No."]
        .astype(int)
        .tolist()
    )


    st.session_state.review = [
        n
        for n in st.session_state.review
        if n in valid_ids
    ]


    if not st.session_state.review:

        st.success(
            "현재 복습할 단어가 없어요. 🎉"
        )

    else:

        review_df = df[
            df["No."].isin(
                st.session_state.review
            )
        ][
            [
                "Word",
                "Korean meaning (뜻)",
                "Level"
            ]
        ]


        st.write(
            f"**복습할 단어: "
            f"{len(review_df)}개**"
        )


        st.dataframe(
            review_df,
            use_container_width=True,
            hide_index=True
        )


        if st.button(
            "🗑️ 복습 목록 비우기",
            key="clear_review",
            use_container_width=True
        ):

            st.session_state.review = []

            st.rerun()


st.divider()

st.caption(
    "G6 Mini-project · "
    "Full 3,000-word vocabulary CSV connected"
)
