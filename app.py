import streamlit as st
from docx import Document
from io import BytesIO

# ---------------------------
# 객관식 퀴즈 + 템플릿 매핑
# ---------------------------

EXPERIMENTS = {
    "STZ Injection": {
        "quiz": [
            {
                "question": "STZ는 어떤 질환을 유도하기 위해 사용되는가?",
                "options": ["고혈압", "당뇨병", "간염", "골다공증"],
                "answer": "당뇨병"
            },
            {
                "question": "STZ 주사액 제조 시 사용되는 완충액은?",
                "options": ["PBS", "Tris-HCl", "시트르산", "HEPES"],
                "answer": "시트르산"
            }
        ],
        "template": "templates/STZ.docx"
    },
    "PCR": {
        "quiz": [
            {
                "question": "PCR의 목적은 무엇인가?",
                "options": ["RNA 합성", "DNA 증폭", "단백질 분리", "세포 배양"],
                "answer": "DNA 증폭"
            },
            {
                "question": "PCR 반응에 필요한 효소는?",
                "options": ["Trypsin", "Taq polymerase", "Ligase", "RNase"],
                "answer": "Taq polymerase"
            }
        ],
        "template": "templates/PCR.docx"
    },
    "Cell Culture": {
        "quiz": [
            {
                "question": "세포 배양 시 CO₂ 인큐베이터의 일반적인 설정 온도는?",
                "options": ["25°C", "30°C", "37°C", "42°C"],
                "answer": "37°C"
            },
            {
                "question": "계대배양 시 세포 부착을 떨어뜨리기 위해 사용하는 효소는?",
                "options": ["Collagenase", "Trypsin", "Proteinase K", "Pepsin"],
                "answer": "Trypsin"
            }
        ],
        "template": "templates/CellCulture.docx"
    },
    "Western Blot": {
        "quiz": [
            {
                "question": "Western blot에서 단백질을 분리하는 데 사용하는 겔은?",
                "options": ["아가로스 겔", "SDS-PAGE", "Native gel", "Acrylamide gel"],
                "answer": "SDS-PAGE"
            },
            {
                "question": "Western blot에서 단백질 검출에 사용되는 항체는?",
                "options": ["1차 항체", "2차 항체", "IgE", "IgM"],
                "answer": "1차 항체"
            }
        ],
        "template": "templates/WesternBlot.docx"
    }
}

# ---------------------------
# 문서 로드 함수
# ---------------------------

def load_docx(path):
    try:
        return Document(path)
    except Exception as e:
        st.error(f"📂 템플릿 로드 실패: {e}")
        return None

def docx_to_bytes(doc):
    buf = BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

# ---------------------------
# Streamlit 앱
# ---------------------------

st.title("🧪 랩 실습 교육 콘텐츠 자동 생성기")
st.caption("실험을 선택하면 객관식 퀴즈와 보고서 템플릿을 자동 생성합니다.")

exp_name = st.selectbox("🔬 실험 선택", list(EXPERIMENTS.keys()))

if exp_name:
    st.subheader("📋 객관식 퀴즈")
    quiz_list = EXPERIMENTS[exp_name]["quiz"]
    score = 0

    for i, q in enumerate(quiz_list):
        selected = st.radio(f"{i+1}. {q['question']}", q["options"], key=f"{exp_name}_{i}")
        if selected == q["answer"]:
            score += 1

    st.success(f"정답 수: {score} / {len(quiz_list)}")

    st.subheader("📄 보고서 템플릿 다운로드")
    doc = load_docx(EXPERIMENTS[exp_name]["template"])
    if doc:
        st.download_button(
            label="📥 템플릿 다운로드",
            data=docx_to_bytes(doc),
            file_name=f"{exp_name.replace(' ', '_')}_report.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
