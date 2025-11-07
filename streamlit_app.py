import streamlit as st
import random

st.set_page_config(page_title="연습: 덧셈·뺄셈 → (조건부) 곱셈·나눗셈", page_icon="🎯")

def generate_question(stage):
    if stage == 1:
        a = random.randint(0, 20)
        b = random.randint(0, 20)
        op = random.choice(["+", "-"])
        if op == "-" and a < b:
            a, b = b, a
        answer = a + b if op == "+" else a - b
        return {"a": a, "b": b, "op": op, "answer": answer}
    else:  # stage 2: multiplication / integer division
        op = random.choice(["*", "/"])
        if op == "*":
            a = random.randint(0, 12)
            b = random.randint(0, 12)
            answer = a * b
            return {"a": a, "b": b, "op": op, "answer": answer}
        else:  # ensure integer division
            divisor = random.randint(1, 12)
            quotient = random.randint(1, 12)
            dividend = divisor * quotient
            a = dividend
            b = divisor
            answer = quotient
            return {"a": a, "b": b, "op": "/", "answer": answer}

# 초기화
if "stage" not in st.session_state:
    st.session_state.stage = 1  # 1: 덧셈/뺄셈, 2: 곱셈/나눗셈
    st.session_state.q_idx = 0
    st.session_state.score = 0
    st.session_state.current = generate_question(1)
    st.session_state.last_feedback = None
    st.session_state.stage1_score = None

st.title("연습: 1단계 → 조건부 2단계")
st.write("1단계(덧셈·뺄셈)를 먼저 3문제 풀고, 모두 맞히면 2단계(곱셈·나눗셈)가 열립니다.")

def handle_submission(user_ans):
    q = st.session_state.current
    correct = q["answer"]
    if int(user_ans) == int(correct):
        st.session_state.score += 1
        st.success("정답입니다!")
        st.session_state.last_feedback = True
    else:
        st.error(f"틀렸습니다. 정답은 {correct} 입니다.")
        st.session_state.last_feedback = False
    st.session_state.q_idx += 1
    # 다음 문제 생성 (다음 단계 진입 전까지)
    if st.session_state.q_idx < 3:
        st.session_state.current = generate_question(st.session_state.stage)
    st.experimental_rerun()

# 페이지 흐름
if st.session_state.stage == 1:
    st.header("1단계: 덧셈·뺄셈 (3문제)")
    if st.session_state.q_idx < 3:
        q = st.session_state.current
        st.markdown(f"### 문제 {st.session_state.q_idx + 1} / 3")
        st.write(f"문제: **{q['a']} {q['op']} {q['b']} = ?**")
        with st.form(key=f"form_1_{st.session_state.q_idx}"):
            user_ans = st.number_input("정수로 답 입력", step=1, format="%d", value=0)
            submitted = st.form_submit_button("확인")
        if submitted:
            handle_submission(user_ans)
    else:
        # 1단계 결과
        st.markdown("## 1단계 결과")
        st.write(f"총 3문제 중 **{st.session_state.score}점** 맞혔습니다.")
        st.session_state.stage1_score = st.session_state.score
        if st.session_state.score == 3:
            st.success("축하합니다! 1단계 만점입니다. 2단계가 열립니다.")
            if st.button("2단계 시작 (곱셈·나눗셈)"):
                st.session_state.stage = 2
                st.session_state.q_idx = 0
                st.session_state.score = 0
                st.session_state.current = generate_question(2)
                st.session_state.last_feedback = None
                st.experimental_rerun()
        else:
            st.info("1단계를 모두 맞혀야 2단계가 열립니다. 다시 도전해보세요.")
            if st.button("1단계 다시하기"):
                st.session_state.q_idx = 0
                st.session_state.score = 0
                st.session_state.current = generate_question(1)
                st.session_state.last_feedback = None
                st.experimental_rerun()

elif st.session_state.stage == 2:
    st.header("2단계: 곱셈·나눗셈 (3문제)")
    if st.session_state.q_idx < 3:
        q = st.session_state.current
        st.markdown(f"### 문제 {st.session_state.q_idx + 1} / 3")
        op_display = "÷" if q["op"] == "/" else "×"
        st.write(f"문제: **{q['a']} {op_display} {q['b']} = ?**")
        with st.form(key=f"form_2_{st.session_state.q_idx}"):
            user_ans = st.number_input("정수로 답 입력", step=1, format="%d", value=0)
            submitted = st.form_submit_button("확인")
        if submitted:
            handle_submission(user_ans)
    else:
        st.markdown("## 2단계 결과")
        st.write(f"총 3문제 중 **{st.session_state.score}점** 맞혔습니다.")
        if st.session_state.score == 3:
            st.balloons()
            st.success("2단계도 모두 맞히셨습니다! 잘하셨어요.")
        if st.button("처음부터 다시하기"):
            st.session_state.stage = 1
            st.session_state.q_idx = 0
            st.session_state.score = 0
            st.session_state.current = generate_question(1)
            st.session_state.last_feedback = None
            st.session_state.stage1_score = None
            st.experimental_rerun()
