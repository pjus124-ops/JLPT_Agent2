import streamlit as st
from datetime import date

st.set_page_config(page_title="JLPT Study Agent")

# =========================
# Session State 초기화
# =========================
if "day" not in st.session_state:
    st.session_state.day = 1

if "history" not in st.session_state:
    st.session_state.history = []

if "generated" not in st.session_state:
    st.session_state.generated = False

if "current_plan" not in st.session_state:
    st.session_state.current_plan = []

# =========================
# 제목
# =========================
st.title("📚 JLPT Study Agent")

# =========================
# 목표 설정
# =========================
level = st.selectbox("목표 등급", ["N5", "N4", "N3", "N2", "N1"])

exam_date = st.date_input("시험 날짜")

today = date.today()
d_day = (exam_date - today).days

st.info(f"📅 JLPT 시험까지 D-{d_day}")

st.divider()

# =========================
# 현재 수준 진단
# =========================
st.subheader("현재 수준 진단")

q1 = st.radio("Q1. 「食べる」의 뜻은?", ["보다", "먹다", "가다"])
q2 = st.radio("Q2. 「学校」의 뜻은?", ["회사", "학교", "병원"])
q3 = st.radio("Q3. 「今日」의 뜻은?", ["내일", "오늘", "어제"])

# =========================
# 진단
# =========================
if st.button("수준 진단 및 계획 생성"):

    score = 0

    if q1 == "먹다":
        score += 1
    if q2 == "학교":
        score += 1
    if q3 == "오늘":
        score += 1

    st.session_state.score = score
    st.session_state.generated = True

    if score == 3:
        st.session_state.current_plan = [
            "단어 30개",
            "문법 2개",
            "독해 2지문",
            "청해 15분"
        ]

    elif score == 2:
        st.session_state.current_plan = [
            "단어 20개",
            "문법 1개",
            "독해 1지문"
        ]

    else:
        st.session_state.current_plan = [
            "단어 10개",
            "히라가나 복습",
            "기초 문법"
        ]

# =========================
# 결과 출력
# =========================
if st.session_state.generated:

    st.success(f"점수: {st.session_state.score}/3")

    if st.session_state.score == 3:
        st.write("현재 수준: N4 수준")
    elif st.session_state.score == 2:
        st.write("현재 수준: N5 상위")
    else:
        st.write("현재 수준: N5 초급")

    st.divider()

    # =========================
    # 현재 계획 출력
    # =========================
    st.subheader(f"DAY {st.session_state.day} 학습 계획")

    for item in st.session_state.current_plan:
        st.write(item)

    st.divider()

    # =========================
    # 학습 결과 입력 (구조화)
    # =========================
    st.subheader("학습 결과 입력")

    subject = st.selectbox("과목", ["단어", "문법", "독해", "청해"])
    result = st.selectbox("결과", ["완료", "못함"])
    detail = st.text_input("상세 (예: 20개, 1지문)")

    if st.button("결과 저장"):

        st.session_state.history.append({
            "day": st.session_state.day,
            "subject": subject,
            "result": result,
            "detail": detail
        })

        st.success("저장 완료")

    # =========================
    # 다음 계획 생성 (핵심 로직)
    # =========================
    st.subheader(f"DAY {st.session_state.day + 1} 추천 계획")

    logs = st.session_state.history

    next_plan = None

    # ✔ 독해 부족
    if any(x["subject"] == "독해" and x["result"] == "못함" and x["day"] == st.session_state.day for x in logs):

        next_plan = [
            "독해 2지문",
            "단어 15개",
            "문법 1개"
        ]

        st.warning("독해 부족")

    # ✔ 단어 부족
    elif any(x["subject"] == "단어" and x["result"] == "못함" and x["day"] == st.session_state.day for x in logs):

        next_plan = [
            "단어 40개",
            "문법 1개",
            "독해 1지문"
        ]

        st.warning("단어 부족")

    # ✔ 문법 부족
    elif any(x["subject"] == "문법" and x["result"] == "못함" and x["day"] == st.session_state.day for x in logs):

        next_plan = [
            "단어 15개",
            "문법 2개",
            "독해 1지문"
        ]

        st.warning("문법 부족")

    # ✔ 정상
    else:

        next_plan = [
            "단어 25개",
            "문법 2개",
            "청해 15분"
        ]

        st.success("잘 수행됨")

    # =========================
    # 출력 (무조건 안전)
    # =========================
    for item in next_plan:
        st.write(item)

    # =========================
    # 다음 DAY 확정
    # =========================
    if st.button("다음 DAY로 이동"):

        st.session_state.current_plan = next_plan
        st.session_state.day += 1

        st.rerun()

# =========================
# 기록 출력
# =========================
if st.session_state.history:

    st.divider()
    st.subheader("학습 기록")

    for h in st.session_state.history:
        st.write(f"DAY{h['day']} - {h['subject']} : {h['result']} ({h['detail']})")