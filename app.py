import streamlit as st
import json
from docx import Document
from io import BytesIO

# 앱 제목
st.title("🧪 랩 실습 퀴즈 및 보고서 생성기")
st.markdown("실험을 선택하면 퀴즈와 보고서 템플릿이 자동 생성됩니다.")

# 실험 목록
experiment_list = ["STZ 주사액 제조", "PCR", "Cell culture", "Western blot"]
selected_exp = st.selectbox("🔬 실험을 선택하세요", experiment_list)

# 퀴즈 데이터 로드
try:
    with open("data/quiz_data.json", "r", encoding="utf-8") as f:
        quiz_data = json.load(f)
except FileNotFoundError:
    st.error("⚠️ 퀴즈 데이터 파일이 없습니다. 'data/quiz_data.json'을 확인하세요.")
    st.stop()

quiz = quiz_data.get(selected_exp, [])
if not quiz:
    st.warning("해당 실험에 대한 퀴즈가 준비되지 않았습니다.")
else:
    st.subheader("📘 퀴즈")
    score = 0
    user_answers = []

    for idx, q in enumerate(quiz):
        st.markdown(f"**Q{idx + 1}. {q['question']}**")
        if q["type"] == "mcq":
            answer = st.radio("선택하세요", q["options"], key=idx)
        else:
            answer = st.text_input("답을 입력하세요", key=idx)
        user_answers.append(answer)

    if st.button("✅ 정답 확인"):
        for idx, q in enumerate(quiz):
            if q["type"] == "mcq":
                correct = q["answer"]
                if user_answers[idx] == correct:
                    score += 1
                    st.success(f"Q{idx + 1} 정답!")
                else:
                    st.error(f"Q{idx + 1} 오답 ❌ (정답: {correct})")
            else:
                st.info(f"Q{idx + 1}는 주관식입니다. 직접 확인하세요.")
        st.markdown(f"🎯 총 점수: **{score} / {len(quiz)}**")

# 보고서 템플릿 다운로드
st.subheader("📄 보고서 템플릿 다운로드")

template_path = f"templates/{selected_exp.replace(' ', '')}.docx"

def load_docx(path):
    try:
        doc = Document(path)
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        return buffer
    except Exception as e:
        st.error(f"📂 템플릿을 불러올 수 없습니다: {e}")
        return None

docx_file = load_docx(template_path)
if docx_file:
    st.download_button(
        label="📥 보고서 템플릿 다운로드 (.docx)",
        data=docx_file,
        file_name=f"{selected_exp.replace(' ', '')}_Report.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
