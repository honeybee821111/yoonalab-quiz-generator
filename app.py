import streamlit as st

# --------------------------
# 실험 정보와 퀴즈 정의
# --------------------------

experiments = {
    "STZ 주사액 제조": {
        "summary": [
            "🧪 STZ란?",
            "• 췌장의 β세포를 선택적으로 파괴하여 당뇨병을 유도하는 실험용 화학물질입니다.",
            "• 보통 0.1M Citrate Buffer (pH 4.5)에 녹여 즉시 사용합니다.",
            "• STZ는 빛과 수분에 불안정하므로 냉장보관하며, 가능한 한 빠르게 투여해야 합니다.",
            "",
            "📌 실험 유의사항",
            "• 마우스 체중 측정 후 용량 계산 (예: 180 mg/kg 기준)",
            "• STZ 제조 후 15분 내 투여 권장",
            "• STZ 조제는 보호구 착용 및 생물안전작업대(BSC) 내에서 수행"
        ],
        "checklist": [
            "STZ 냉장 보관 여부 확인",
            "체중 측정 및 정확한 용량 계산 완료",
            "0.1M Citrate Buffer 준비 및 pH 확인",
            "STZ 제조 후 즉시 사용 (15분 내)",
            "BSC 내에서 조제 및 주사 실시",
            "주사 후 개체 상태 모니터링 계획 수립"
        ],
        "quiz": [
            {
                "question": "STZ는 어떤 세포를 주로 파괴하는가?",
                "options": ["α세포", "β세포", "T세포", "간세포"],
                "answer": "β세포",
                "explanation": "STZ는 췌장의 인슐린 분비 β세포를 선택적으로 파괴하여 고혈당을 유도합니다."
            },
            {
                "question": "STZ 용해에 가장 적절한 완충 용액은?",
                "options": ["PBS", "0.9% NaCl", "Citrate Buffer", "RPMI"],
                "answer": "Citrate Buffer",
                "explanation": "0.1M Citrate Buffer (pH 4.5)는 STZ의 안정성을 유지하는 데 적합합니다."
            },
            {
                "question": "STZ 제조 후 언제 사용하는 것이 권장되는가?",
                "options": ["3시간 이내", "제조 직후", "24시간 이내", "냉동 보관 후 해동"],
                "answer": "제조 직후",
                "explanation": "STZ는 수분에 불안정하므로 제조 후 15분 내 사용이 가장 바람직합니다."
            }
        ]
    },

    "PCR (Polymerase Chain Reaction)": {
        "summary": [
            "🧪 PCR이란?",
            "• 특정 DNA 서열을 증폭하는 분자생물학 기술입니다.",
            "• 주로 유전자 확인, 돌연변이 분석, 병원체 탐지에 사용됩니다.",
            "",
            "📌 실험 유의사항",
            "• 정확한 primer와 template DNA 사용",
            "• 마스터믹스 조제 후 ice 위에서 작업 유지",
            "• 오염 방지를 위한 무균 작업 환경 유지"
        ],
        "checklist": [
            "Template DNA 준비",
            "Primer set 확인",
            "PCR Master mix 조제",
            "PCR 조건 세팅 (denaturation, annealing, extension)",
            "Amplicon 크기 확인 계획 수립"
        ],
        "quiz": [
            {
                "question": "PCR 반응에 반드시 포함되어야 하는 구성 요소가 아닌 것은?",
                "options": ["dNTP", "Primer", "DNA polymerase", "RNase"],
                "answer": "RNase",
                "explanation": "RNase는 RNA 분해효소로 PCR 반응에는 필요하지 않습니다."
            },
            {
                "question": "PCR에서 annealing 단계는 무엇을 의미하는가?",
                "options": ["DNA 중합", "DNA 열변성", "Primer 결합", "단백질 번역"],
                "answer": "Primer 결합",
                "explanation": "Annealing 단계는 primer가 template DNA에 결합하는 온도 구간입니다."
            }
        ]
    },

    "Cell Culture": {
        "summary": [
            "🧫 Cell culture란?",
            "• 세포를 인공적으로 배양액과 환경에서 증식시키는 기초 실험 기법입니다.",
            "",
            "📌 실험 유의사항",
            "• 무균 환경 유지 (BSC 사용)",
            "• 배지 교체 주기 확인 및 배양기 온도/CO₂ 유지",
            "• 오염 여부 육안 확인 및 mycoplasma test 정기 수행"
        ],
        "checklist": [
            "배지 및 시약 준비",
            "세포 상태 확인 (현미경)",
            "세포 수 계산 및 split 계획",
            "CO₂ 인큐베이터 상태 확인",
            "폐기물 및 오염 방지 수칙 점검"
        ],
        "quiz": [
            {
                "question": "Cell culture에서 CO₂는 왜 필요한가?",
                "options": ["산소 공급", "온도 조절", "pH 조절", "세포 고정"],
                "answer": "pH 조절",
                "explanation": "CO₂는 배지의 중탄산 완충 시스템과 반응하여 pH를 조절합니다."
            },
            {
                "question": "세포 배양 시 가장 흔한 오염 원인은?",
                "options": ["세포 증식", "핵 분열", "무균 불량", "고온 배양"],
                "answer": "무균 불량",
                "explanation": "배양 과정 중 무균 작업이 지켜지지 않으면 오염이 발생합니다."
            }
        ]
    },

    "Western Blot": {
        "summary": [
            "🧬 Western blot이란?",
            "• 단백질을 검출하고 정량화하는 전기영동 기반 실험 기법입니다.",
            "",
            "📌 실험 유의사항",
            "• 정확한 단백질 정량 (BCA or Bradford)",
            "• 적절한 gel 농도 선택",
            "• 항체 희석과 incubation 조건 최적화"
        ],
        "checklist": [
            "단백질 추출 및 정량 완료",
            "SDS-PAGE 준비 및 로딩",
            "Transfer 조건 설정",
            "Blocking 및 1차 항체/2차 항체 반응 준비",
            "Detection 방법 (chemiluminescence 등) 확인"
        ],
        "quiz": [
            {
                "question": "Western blot에서 1차 항체의 역할은?",
                "options": ["단백질 전기영동", "단백질에 특이적 결합", "전하 이동", "빛 방출"],
                "answer": "단백질에 특이적 결합",
                "explanation": "1차 항체는 검출하고자 하는 표적 단백질에 특이적으로 결합합니다."
            },
            {
                "question": "Transfer 단계의 목적은?",
                "options": ["단백질 분해", "Gel 생성", "막으로 이동", "항체 희석"],
                "answer": "막으로 이동",
                "explanation": "단백질을 gel에서 membrane으로 전이시켜 항체 검출이 가능하도록 합니다."
            }
        ]
    }
}

# 앱 인터페이스 생성
st.title("🧪 랩 실습 퀴즈 학습기")
selected_exp = st.selectbox("실험을 선택하세요", list(experiments.keys()))

if selected_exp:
    exp = experiments[selected_exp]

    st.header("📘 요약 카드")
    for line in exp["summary"]:
        st.markdown(line)

    st.divider()
    st.header("🧾 실습 체크리스트")
    for item in exp["checklist"]:
        st.checkbox(item)

    st.divider()
    st.header("❓ 객관식 퀴즈")

    score = 0
    answers = []

    for idx, item in enumerate(exp["quiz"]):
        st.subheader(f"Q{idx + 1}. {item['question']}")
        user_answer = st.radio("답을 선택하세요:", item["options"], key=f"q{selected_exp}_{idx}")
        answers.append((user_answer, item["answer"], item["explanation"]))

    st.divider()

    if st.button("📊 점수 확인"):
        for user, correct, _ in answers:
            if user == correct:
                score += 1

        percent = int(score / len(answers) * 100)
        st.subheader(f"✅ 당신의 점수: {percent}점")

        for idx, (user, correct, explanation) in enumerate(answers):
            result = "🟢 정답" if user == correct else "🔴 오답"
            st.markdown(f"**Q{idx + 1}**: {result}  \n정답: {correct}  \n해설: {explanation}")

        if percent >= 80:
            st.success("이 실험에 대한 이해도가 높습니다! 🔬")
        elif percent >= 50:
            st.info("기본 개념은 이해했지만, 복습이 필요합니다.")
        else:
            st.error("학습이 더 필요합니다. 요약 카드와 다시 학습해보세요.")
