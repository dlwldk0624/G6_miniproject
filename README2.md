# Group Vocabulary App — Streamlit Version

## 1. Group Information
- Group: 6
- Members (역할):
  - 이지아 (단어 파일, 코드 생성 및 관리)
  - 정예원 (Streamlit 관련 업무)
  - 최동빈 (기록자)
  - 김한일 (팀원)
- Project link:
  https://github.com/dlwldk0624/G6_miniproject

## 2. Target Learners
Who is this app designed for? (한국 학습자 기준으로 정보를 바꿀 것: 예) 중1, 고2)
- This app is designed for **Korean Grade 7 learners (중학교 1학년 학생)**.

## 3. Learning Goal
What should learners practice or learn?
- The goal of this app is to help learners develop basic English vocabulary knowledge through **repeated exposure and retrieval practice**.
- Learners practice understanding word meanings, recalling English spellings from Korean meanings, listening to word pronunciation, and reviewing words they answered incorrectly.

## 4. What We Updated
Write what you changed from the first version. Use lists.
- Rebuilt the previous HTML/CSS/JavaScript prototype as a **single-page Streamlit app**.
- Expanded the vocabulary data from about **10 sample words to the full 3,000-word vocabulary list**.
- Connected the app to an external **CSV file** instead of storing vocabulary directly in the code.
- Added vocabulary level selection: **All, Elementary, MidHigh, Extended**.
- Added a data check to confirm that all **3,000 vocabulary items** are loaded correctly.
- Kept and improved the main learning activities: **Flashcards, Meaning Quiz, Spelling Practice, and Review Again**.
- Added **English pronunciation using TTS (gTTS)**.
- Improved Spelling Practice so learners can type an answer and press **Enter** to submit it and move to the next question.
- Automatically saves incorrectly answered words to the **Review Again** list.
- Increased the size of words, buttons, and input boxes to improve readability and mobile usability.
- Fixed CSV file loading, file-path, and Streamlit deployment errors found during testing.

## 5. Main Features
List the main 3–4 features.
1. **Flashcards**  
   Learners see an English word, recall its meaning, and then check the Korean meaning and pronunciation.

2. **Meaning Quiz**  
   Learners choose the correct Korean meaning for an English word from multiple choices.

3. **Spelling Practice**  
   Learners see a Korean meaning and type the corresponding English word from memory. They can press Enter to submit the answer.

4. **Review Again**  
   Words answered incorrectly in the Meaning Quiz or Spelling Practice are collected for additional review.

## 6. Vocabulary Data
Explain how the app uses the CSV file. 앱에 사용된 데이터 파일(csv) 링크도 꼭 포함시킬 것.
- The app loads vocabulary directly from the CSV file using **pandas**.

- The dataset contains **3,000 unique vocabulary items**:
  - Elementary: 800 words
  - MidHigh: 1,200 words
  - Extended: 1,000 words

- The app uses information such as the English word, Korean meaning, vocabulary level, and related vocabulary or variation information. Learners can select a vocabulary level, and when **All** is selected, the full 3,000-word dataset is used as the learning pool.

- CSV file:  
[vocabulary.csv](./vocabulary.csv)

## 7. What We Learned Through This Group Activity
Write 2–4 sentences.
Through this group activity, we learned how to develop an HTML vocabulary prototype into a data-connected Streamlit application. We also learned how to connect and manage a large CSV vocabulary dataset and use it in different learning activities. During deployment, we solved several problems related to file names, file paths, and Streamlit settings. This process helped us understand the importance of testing and debugging when developing an educational application.

## 8. Streamlit App
[Open our Streamlit app](https://vocab-life.streamlit.app/)
