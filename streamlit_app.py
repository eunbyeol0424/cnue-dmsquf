import streamlit as st
import random

st.set_page_config(page_title="덧셈/뺄셈 연습", page_icon="🎯")

def generate_question():
    a = random.randint(0, 20)
    b = random.randint(0, 20)
    op = random.choice(["+", "-"])
    if op == "-" and a < b:
        a, b = b, a
    answer = a + b if op == "+" else a - b
    return {"a": a, "b": b, "op": op, "answer": answer}

if "q_idx" not in st.session_state:
    st.session_state.q_idx = 0
    st.session_state.score = 0
    st.session_state.current = generate_question()
    st.session_state.last_feedback = None

st.title("덧셈·뺄셈 3문제 연속 연습")
st.write("아래 문제를 순서대로 풀고 제출 버튼을 누르세요. 총 3문제 후 정답 개수를 알려드립니다.")

if st.session_state.q_idx < 3:
    q = st.session_state.current
    st.markdown(f"### 문제 {st.session_state.q_idx + 1} / 3")
    st.write(f"문제: **{q['a']} {q['op']} {q['b']} = ?**")
    with st.form(key=f"form_{st.session_state.q_idx}"):
        user_ans = st.number_input("정수로 답 입력", step=1, format="%d", value=0)
        submitted = st.form_submit_button("확인")
    if submitted:
        correct = q["answer"]
        if int(user_ans) == int(correct):
            st.session_state.score += 1
            st.success("정답입니다!")
            st.session_state.last_feedback = True
        else:
            st.error(f"틀렸습니다. 정답은 {correct} 입니다.")
            st.session_state.last_feedback = False
        st.session_state.q_idx += 1
        if st.session_state.q_idx < 3:
            st.session_state.current = generate_question()
        st.experimental_rerun()
else:
    st.markdown("## 결과")
    st.write(f"총 3문제 중 **{st.session_state.score}점** 맞혔습니다.")
    if st.session_state.score == 3:
        st.balloons()
    if st.button("다시 시작"):
        st.session_state.q_idx = 0
        st.session_state.score = 0
        st.session_state.current = generate_question()
        st.session_state.last_feedback = None
        st.experimental_rerun()
