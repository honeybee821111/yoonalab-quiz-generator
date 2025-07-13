import streamlit as st
from docx import Document
from io import BytesIO

# 앱 제목
st.title("🧪 랩 실습 퀴즈 및 보고서 생성기")
st.markdown("실험을 선택하면 퀴즈와 보고서 템플릿이 자동 생성됩니다.")

# 실험 목록
experiment_list = ["STZ 주사액 제조", "PCR", "Cell culture", "Western blot"]
selected_exp = st.selectbox("🔬 실험을 선택하세요", experiment_list)

# ✅ 외부 파일 없이 내부 딕셔너리로 퀴즈 구성
quiz_data = {
    "STZ 주사액 제조": [
        {
            "type": "mcq",
            "question": "STZ 완충액 제조에 가장 많이 사용되는 pH는?",
            "options": ["pH 3.0", "pH 4.5", "pH 7.0", "pH 9.0"],
            "answer": "pH 4.5"
        },
        {
            "type": "mcq",
            "question": "STZ 주사액은 사용 직전에 제조해야 하는 이유는?",
            "options": ["온도에 민감해서", "빛에 민감해서", "수분에 의해 분해되기 때문", "냄새가 나서"],
            "answer": "수분에 의해 분해되기 때문"
        },
        {
            "type": "subjective",
            "question": "STZ 주사 전 금식이 필요한 이유를 서술하시오."
        }
    ],
    "PCR": [
        {
            "type": "mcq",
            "question": "PCR의 기본 구성 요소가 아닌 것은?",
            "options": ["dNTP", "Primer", "DNA polymerase", "Ligase"],
            "answer": "Ligase"
        },
        {
            "type": "subjective",
            "question": "PCR에서 negative control이 중요한 이유를 서술하시오."
        }
    ],
    "Cell culture": [
        {
            "type": "mcq",
            "question": "일반적인 세포배양 조건에서 CO₂ 농도는?",
            "options": ["0%", "2%", "5%", "10%"],
            "answer": "5%"
        },
        {
            "type": "subjective",
            "question": "세포 배양 시 오염을 방지하기 위한 기본 수칙을 쓰시오."
        }
    ],
    "Western blot": [
        {
            "type": "mcq",
            "question": "Western blot에서 단백질 전이에 사용하는 막은?",
            "options": ["PVDF", "Cellulose", "Nylon", "Nitrocellulose"],
            "answer": "PVDF"
        },
        {
            "type": "subjective",
            "question": "비특이적 밴드가 나타날 경우의 대처 방안을 서술하시오."
        }
    ]
}

# 퀴즈 출력
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
