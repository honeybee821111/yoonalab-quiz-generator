import streamlit as st
import json
import time
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, List, Any
import base64

# 페이지 설정
st.set_page_config(
    page_title="🧪 랩 실습 퀴즈 학습기",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 세션 상태 초기화
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {
        'name': '',
        'level': 'beginner',
        'quiz_history': [],
        'favorites': [],
        'weak_areas': [],
        'study_streak': 0,
        'total_points': 0
    }

if 'current_quiz_state' not in st.session_state:
    st.session_state.current_quiz_state = {
        'answers': [],
        'start_time': None,
        'timer_enabled': False,
        'time_limit': 300  # 5분
    }

# 실험 데이터 (확장됨)
experiments = {
    "STZ 주사액 제조": {
        "difficulty": "intermediate",
        "category": "동물실험",
        "image_url": "https://via.placeholder.com/400x200?text=STZ+Injection",
        "video_url": "https://example.com/stz_video",
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
        "protocol_steps": [
            "1. 마우스 체중 측정 및 기록",
            "2. 0.1M Citrate Buffer (pH 4.5) 준비",
            "3. STZ 파우더를 정확히 계량",
            "4. Buffer에 STZ 용해 (vortex 사용)",
            "5. 15분 내 복강 주사 실시",
            "6. 주사 후 개체 상태 모니터링"
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
                "explanation": "STZ는 췌장의 인슐린 분비 β세포를 선택적으로 파괴하여 고혈당을 유도합니다.",
                "difficulty": "easy"
            },
            {
                "question": "STZ 용해에 가장 적절한 완충 용액은?",
                "options": ["PBS", "0.9% NaCl", "Citrate Buffer", "RPMI"],
                "answer": "Citrate Buffer",
                "explanation": "0.1M Citrate Buffer (pH 4.5)는 STZ의 안정성을 유지하는 데 적합합니다.",
                "difficulty": "medium"
            },
            {
                "question": "STZ 제조 후 언제 사용하는 것이 권장되는가?",
                "options": ["3시간 이내", "제조 직후", "24시간 이내", "냉동 보관 후 해동"],
                "answer": "제조 직후",
                "explanation": "STZ는 수분에 불안정하므로 제조 후 15분 내 사용이 가장 바람직합니다.",
                "difficulty": "medium"
            },
            {
                "question": "STZ 주사 시 가장 적절한 투여 경로는?",
                "options": ["정맥주사", "근육주사", "복강주사", "피하주사"],
                "answer": "복강주사",
                "explanation": "STZ는 일반적으로 복강주사(IP)로 투여하여 전신 흡수를 유도합니다.",
                "difficulty": "hard"
            }
        ],
        "interactive_quiz": {
            "type": "drag_drop",
            "question": "STZ 실험 순서를 올바르게 배열하세요:",
            "items": ["체중 측정", "Buffer 준비", "STZ 용해", "주사 실시", "상태 모니터링"],
            "correct_order": [0, 1, 2, 3, 4]
        }
    },
    
    "PCR (Polymerase Chain Reaction)": {
        "difficulty": "beginner",
        "category": "분자생물학",
        "image_url": "https://via.placeholder.com/400x200?text=PCR+Machine",
        "video_url": "https://example.com/pcr_video",
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
        "protocol_steps": [
            "1. Template DNA 준비 및 농도 측정",
            "2. Primer 설계 및 준비",
            "3. PCR Master mix 조제",
            "4. PCR 조건 설정 (94°C-55°C-72°C)",
            "5. 열순환 반응 실시",
            "6. Gel 전기영동으로 결과 확인"
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
                "explanation": "RNase는 RNA 분해효소로 PCR 반응에는 필요하지 않습니다.",
                "difficulty": "easy"
            },
            {
                "question": "PCR에서 annealing 단계는 무엇을 의미하는가?",
                "options": ["DNA 중합", "DNA 열변성", "Primer 결합", "단백질 번역"],
                "answer": "Primer 결합",
                "explanation": "Annealing 단계는 primer가 template DNA에 결합하는 온도 구간입니다.",
                "difficulty": "medium"
            },
            {
                "question": "PCR의 변성(denaturation) 단계에서 일반적인 온도는?",
                "options": ["55°C", "72°C", "94°C", "37°C"],
                "answer": "94°C",
                "explanation": "94°C에서 DNA 이중나선이 분리되어 단일가닥이 됩니다.",
                "difficulty": "medium"
            }
        ],
        "interactive_quiz": {
            "type": "sequence_match",
            "question": "PCR 3단계를 온도와 매칭하세요:",
            "items": ["Denaturation", "Annealing", "Extension"],
            "matches": ["94°C", "55°C", "72°C"]
        }
    },
    
    "Cell Culture": {
        "difficulty": "beginner",
        "category": "세포생물학",
        "image_url": "https://via.placeholder.com/400x200?text=Cell+Culture",
        "video_url": "https://example.com/cell_culture_video",
        "summary": [
            "🧫 Cell culture란?",
            "• 세포를 인공적으로 배양액과 환경에서 증식시키는 기초 실험 기법입니다.",
            "",
            "📌 실험 유의사항",
            "• 무균 환경 유지 (BSC 사용)",
            "• 배지 교체 주기 확인 및 배양기 온도/CO₂ 유지",
            "• 오염 여부 육안 확인 및 mycoplasma test 정기 수행"
        ],
        "protocol_steps": [
            "1. 배지 및 시약 준비 (37°C 예열)",
            "2. BSC 내 무균 환경 세팅",
            "3. 세포 상태 현미경 관찰",
            "4. 배지 교체 또는 계대배양",
            "5. 인큐베이터 보관 (37°C, 5% CO₂)",
            "6. 정기적 상태 확인"
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
                "explanation": "CO₂는 배지의 중탄산 완충 시스템과 반응하여 pH를 조절합니다.",
                "difficulty": "medium"
            },
            {
                "question": "세포 배양 시 가장 흔한 오염 원인은?",
                "options": ["세포 증식", "핵 분열", "무균 불량", "고온 배양"],
                "answer": "무균 불량",
                "explanation": "배양 과정 중 무균 작업이 지켜지지 않으면 오염이 발생합니다.",
                "difficulty": "easy"
            }
        ],
        "interactive_quiz": {
            "type": "drag_drop",
            "question": "세포 배양 과정을 순서대로 배열하세요:",
            "items": ["배지 준비", "BSC 세팅", "세포 관찰", "배지 교체", "인큐베이터 보관"],
            "correct_order": [0, 1, 2, 3, 4]
        }
    },
    
    "Western Blot": {
        "difficulty": "advanced",
        "category": "단백질분석",
        "image_url": "https://via.placeholder.com/400x200?text=Western+Blot",
        "video_url": "https://example.com/western_blot_video",
        "summary": [
            "🧬 Western blot이란?",
            "• 단백질을 검출하고 정량화하는 전기영동 기반 실험 기법입니다.",
            "",
            "📌 실험 유의사항",
            "• 정확한 단백질 정량 (BCA or Bradford)",
            "• 적절한 gel 농도 선택",
            "• 항체 희석과 incubation 조건 최적화"
        ],
        "protocol_steps": [
            "1. 단백질 추출 및 정량",
            "2. SDS-PAGE gel 제작",
            "3. 단백질 로딩 및 전기영동",
            "4. Transfer to membrane",
            "5. Blocking 및 항체 반응",
            "6. Detection 및 이미지 분석"
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
                "explanation": "1차 항체는 검출하고자 하는 표적 단백질에 특이적으로 결합합니다.",
                "difficulty": "medium"
            },
            {
                "question": "Transfer 단계의 목적은?",
                "options": ["단백질 분해", "Gel 생성", "막으로 이동", "항체 희석"],
                "answer": "막으로 이동",
                "explanation": "단백질을 gel에서 membrane으로 전이시켜 항체 검출이 가능하도록 합니다.",
                "difficulty": "medium"
            }
        ],
        "interactive_quiz": {
            "type": "sequence_match",
            "question": "Western blot 과정을 순서대로 매칭하세요:",
            "items": ["단백질 추출", "전기영동", "Transfer", "항체 반응", "Detection"],
            "matches": ["1단계", "2단계", "3단계", "4단계", "5단계"]
        }
    },
    
    "ELISA": {
        "difficulty": "intermediate",
        "category": "면역학",
        "image_url": "https://via.placeholder.com/400x200?text=ELISA+Plate",
        "video_url": "https://example.com/elisa_video",
        "summary": [
            "🧪 ELISA란?",
            "• 효소 연결 면역 흡착 분석법으로 단백질, 항체, 호르몬 등을 정량하는 기법입니다.",
            "• 96-well plate를 사용하여 high-throughput 분석이 가능합니다.",
            "",
            "📌 실험 유의사항",
            "• 표준 곡선 제작을 위한 serial dilution",
            "• 적절한 washing 과정으로 비특이적 결합 제거",
            "• 발색 반응 시간 조절"
        ],
        "protocol_steps": [
            "1. Plate coating with capture antibody",
            "2. Blocking non-specific binding sites",
            "3. 샘플 및 표준물질 첨가",
            "4. Detection antibody 반응",
            "5. Enzyme conjugate 첨가",
            "6. 기질 첨가 후 발색 반응 측정"
        ],
        "checklist": [
            "항체 농도 최적화 완료",
            "표준 곡선용 serial dilution 준비",
            "Washing buffer 및 blocking solution 준비",
            "Plate reader 보정 및 파장 설정",
            "발색 반응 시간 계획 수립"
        ],
        "quiz": [
            {
                "question": "ELISA에서 blocking 단계의 목적은?",
                "options": ["항체 활성화", "비특이적 결합 방지", "효소 반응 촉진", "세포 고정"],
                "answer": "비특이적 결합 방지",
                "explanation": "Blocking은 빈 결합 부위를 차단하여 비특이적 결합을 방지합니다.",
                "difficulty": "medium"
            },
            {
                "question": "ELISA 표준 곡선 제작 시 사용하는 방법은?",
                "options": ["동일 농도 반복", "Serial dilution", "Random sampling", "Single point"],
                "answer": "Serial dilution",
                "explanation": "표준물질을 단계적으로 희석하여 농도-흡광도 곡선을 만듭니다.",
                "difficulty": "easy"
            }
        ],
        "interactive_quiz": {
            "type": "drag_drop",
            "question": "ELISA 과정을 올바른 순서로 배열하세요:",
            "items": ["Coating", "Blocking", "샘플 첨가", "Detection Ab", "효소 반응", "발색"],
            "correct_order": [0, 1, 2, 3, 4, 5]
        }
    },
    
    "Flow Cytometry": {
        "difficulty": "advanced",
        "category": "세포분석",
        "image_url": "https://via.placeholder.com/400x200?text=Flow+Cytometer",
        "video_url": "https://example.com/flow_cytometry_video",
        "summary": [
            "🔬 Flow cytometry란?",
            "• 세포를 개별적으로 분석하여 크기, 복잡도, 형광 특성을 측정하는 기법입니다.",
            "• 세포 집단의 분포, 세포 주기, 아폽토시스 등을 분석할 수 있습니다.",
            "",
            "📌 실험 유의사항",
            "• 단일 세포 현탁액 준비",
            "• 적절한 형광 항체 조합 선택",
            "• Compensation 설정 및 gating 전략 수립"
        ],
        "protocol_steps": [
            "1. 세포 수집 및 단일 현탁액 제작",
            "2. 세포 수 계산 및 농도 조정",
            "3. 형광 항체 staining",
            "4. Flow cytometer 설정 및 compensation",
            "5. 데이터 수집 및 분석",
            "6. 결과 해석 및 통계 분석"
        ],
        "checklist": [
            "세포 viability 확인",
            "형광 항체 농도 최적화",
            "적절한 control 설정",
            "Machine 보정 및 설정 확인",
            "Gating 전략 수립"
        ],
        "quiz": [
            {
                "question": "Flow cytometry에서 FSC는 무엇을 나타내는가?",
                "options": ["세포 복잡도", "세포 크기", "형광 강도", "세포 밀도"],
                "answer": "세포 크기",
                "explanation": "FSC (Forward Scatter)는 세포의 크기를 나타내는 지표입니다.",
                "difficulty": "medium"
            },
            {
                "question": "Compensation의 목적은?",
                "options": ["세포 분리", "형광 겹침 보정", "세포 고정", "항체 활성화"],
                "answer": "형광 겹침 보정",
                "explanation": "서로 다른 형광 채널 간의 spectral overlap을 보정하는 과정입니다.",
                "difficulty": "hard"
            }
        ],
        "interactive_quiz": {
            "type": "sequence_match",
            "question": "Flow cytometry 분석 과정을 매칭하세요:",
            "items": ["세포 준비", "Staining", "기기 설정", "데이터 수집", "분석"],
            "matches": ["샘플 준비", "항체 반응", "보정 및 설정", "측정", "결과 해석"]
        }
    }
}

# 유틸리티 함수들
def save_quiz_result(experiment_name: str, score: int, time_taken: int, difficulty: str):
    """퀴즈 결과를 세션 상태에 저장"""
    result = {
        'experiment': experiment_name,
        'score': score,
        'time_taken': time_taken,
        'difficulty': difficulty,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    st.session_state.user_profile['quiz_history'].append(result)
    st.session_state.user_profile['total_points'] += score

def get_difficulty_color(difficulty: str) -> str:
    """난이도별 색상 반환"""
    colors = {
        'beginner': '#4CAF50',  # 녹색
        'intermediate': '#FF9800',  # 주황색
        'advanced': '#F44336'  # 빨간색
    }
    return colors.get(difficulty, '#757575')

def create_progress_chart():
    """학습 진행률 차트 생성"""
    if not st.session_state.user_profile['quiz_history']:
        return None
    
    df = pd.DataFrame(st.session_state.user_profile['quiz_history'])
    
    # 날짜별 점수 추이
    fig = px.line(df, x='date', y='score', title='📈 학습 진행률')
    fig.update_layout(
        xaxis_title="날짜",
        yaxis_title="점수",
        showlegend=False
    )
    return fig

def create_difficulty_distribution():
    """난이도별 분포 차트"""
    if not st.session_state.user_profile['quiz_history']:
        return None
        
    df = pd.DataFrame(st.session_state.user_profile['quiz_history'])
    difficulty_counts = df['difficulty'].value_counts()
    
    fig = px.pie(
        values=difficulty_counts.values,
        names=difficulty_counts.index,
        title='📊 난이도별 학습 분포'
    )
    return fig

def render_interactive_quiz(quiz_data: Dict[str, Any], exp_name: str):
    """인터랙티브 퀴즈 렌더링"""
    if quiz_data['type'] == 'drag_drop':
        st.subheader("🎯 " + quiz_data['question'])
        
        # 항목들을 랜덤하게 섞어서 표시
        items = quiz_data['items'].copy()
        correct_order = quiz_data['correct_order']
        
        # 사용자가 순서를 선택할 수 있도록 selectbox 사용
        user_order = []
        for i in range(len(items)):
            selected = st.selectbox(
                f"{i+1}번째 단계:",
                items,
                key=f"interactive_{exp_name}_{i}"
            )
            user_order.append(items.index(selected))
        
        if st.button("정답 확인", key=f"check_interactive_{exp_name}"):
            if user_order == correct_order:
                st.success("🎉 정답입니다! 순서를 올바르게 맞추셨습니다.")
            else:
                st.error("❌ 틀렸습니다. 다시 시도해보세요.")
                correct_sequence = [items[i] for i in correct_order]
                st.info(f"정답 순서: {' → '.join(correct_sequence)}")
    
    elif quiz_data['type'] == 'sequence_match':
        st.subheader("🔗 " + quiz_data['question'])
        
        items = quiz_data['items']
        matches = quiz_data['matches']
        
        user_matches = []
        for i, item in enumerate(items):
            selected_match = st.selectbox(
                f"{item}:",
                matches,
                key=f"match_{exp_name}_{i}"
            )
            user_matches.append(selected_match)
        
        if st.button("매칭 확인", key=f"check_match_{exp_name}"):
            if user_matches == matches:
                st.success("🎉 모든 매칭이 정확합니다!")
            else:
                st.error("❌ 일부 매칭이 틀렸습니다.")
                for i, (item, correct, user) in enumerate(zip(items, matches, user_matches)):
                    if correct == user:
                        st.success(f"✅ {item} - {correct}")
                    else:
                        st.error(f"❌ {item} - 정답: {correct}, 선택: {user}")

# 메인 인터페이스
def main():
    # 사이드바 - 사용자 프로필
    with st.sidebar:
        st.header("👤 사용자 프로필")
        
        # 사용자 이름 입력
        user_name = st.text_input("이름", value=st.session_state.user_profile['name'])
        st.session_state.user_profile['name'] = user_name
        
        # 레벨 선택
        level = st.selectbox(
            "레벨",
            ['beginner', 'intermediate', 'advanced'],
            index=['beginner', 'intermediate', 'advanced'].index(st.session_state.user_profile['level'])
        )
        st.session_state.user_profile['level'] = level
        
        # 통계 표시
        st.subheader("📊 학습 통계")
        st.metric("총 점수", st.session_state.user_profile['total_points'])
        st.metric("완료한 퀴즈", len(st.session_state.user_profile['quiz_history']))
        
        # 학습 기록 차트
        if st.session_state.user_profile['quiz_history']:
            progress_chart = create_progress_chart()
            if progress_chart:
                st.plotly_chart(progress_chart, use_container_width=True)
        
        # 즐겨찾기 관리
        st.subheader("⭐ 즐겨찾기")
        favorites = st.session_state.user_profile['favorites']
        if favorites:
            for fav in favorites:
                st.write(f"• {fav}")
        else:
            st.write("즐겨찾기한 실험이 없습니다.")

    # 메인 컨텐츠
    st.title("🧪 랩 실습 퀴즈 학습기")
    
    # 탭 구성
    tab1, tab2, tab3, tab4 = st.tabs(["📚 학습하기", "🎯 퀴즈", "📈 분석", "⚙️ 설정"])
    
    with tab1:
        st.header("🔬 실험 선택")
        
        # 필터링 옵션
        col1, col2 = st.columns(2)
        with col1:
            category_filter = st.selectbox(
                "카테고리",
                ["전체"] + list(set(exp['category'] for exp in experiments.values()))
            )
        with col2:
            difficulty_filter = st.selectbox(
                "난이도",
                ["전체", "beginner", "intermediate", "advanced"]
            )
        
        # 실험 카드 표시
        filtered_experiments = {}
        for name, exp in experiments.items():
            if (category_filter == "전체" or exp['category'] == category_filter) and \
               (difficulty_filter == "전체" or exp['difficulty'] == difficulty_filter):
                filtered_experiments[name] = exp
        
        # 실험 카드들을 그리드로 표시
        cols = st.columns(2)
        for i, (name, exp) in enumerate(filtered_experiments.items()):
            with cols[i % 2]:
                with st.container():
                    st.markdown(f"""
                    <div style="border: 1px solid #ddd; border-radius: 10px; padding: 20px; margin: 10px 0;">
                        <h3>{name}</h3>
                        <p><strong>카테고리:</strong> {exp['category']}</p>
                        <p><strong>난이도:</strong> 
                        <span style="color: {get_difficulty_color(exp['difficulty'])};">
                        {exp['difficulty'].upper()}</span></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"학습하기", key=f"learn_{name}"):
                        st.session_state.selected_experiment = name
                        st.rerun()
                    
                    # 즐겨찾기 토글
                    is_favorite = name in st.session_state.user_profile['favorites']
                    if st.button("⭐" if is_favorite else "☆", key=f"fav_{name}"):
                        if is_favorite:
                            st.session_state.user_profile['favorites'].remove(name)
                        else:
                            st.session_state.user_profile['favorites'].append(name)
                        st.rerun()
        
        # 선택된 실험 상세 보기
        if hasattr(st.session_state, 'selected_experiment'):
            selected_exp = st.session_state.selected_experiment
            exp = experiments[selected_exp]
            
            st.divider()
            st.header(f"📘 {selected_exp} - 학습 자료")
            
            # 실험 이미지 (플레이스홀더)
            st.image(exp['image_url'], caption=f"{selected_exp} 실험", use_column_width=True)
            
            # 비디오 링크
            if exp.get('video_url'):
                st.markdown(f"🎥 [실험 동영상 보기]({exp['video_url']})")
            
            # 요약 정보
            st.subheader("📋 실험 요약")
            for line in exp["summary"]:
                st.markdown(line)
            
            # 프로토콜 단계
            if 'protocol_steps' in exp:
                st.subheader("🔬 실험 프로토콜")
                for step in exp['protocol_steps']:
                    st.markdown(step)
            
            # 체크리스트
            st.subheader("✅ 실습 체크리스트")
            for item in exp["checklist"]:
                st.checkbox(item, key=f"check_{selected_exp}_{item}")
    
    with tab2:
        st.header("🎯 퀴즈 도전!")
        
        # 퀴즈 설정
        col1, col2 = st.columns(2)
        with col1:
            quiz_experiment = st.selectbox(
                "퀴즈 실험 선택",
                list(experiments.keys()),
                key="quiz_selection"
            )
        with col2:
            timer_enabled = st.checkbox("⏰ 타이머 사용", value=False)
            if timer_enabled:
                time_limit = st.slider("제한 시간 (분)", 1, 30, 5)
                st.session_state.current_quiz_state['time_limit'] = time_limit * 60
        
        if quiz_experiment:
            exp = experiments[quiz_experiment]
            
            # 퀴즈 시작
            if st.button("🚀 퀴즈 시작!", key="start_quiz"):
                st.session_state.current_quiz_state['start_time'] = time.time()
                st.session_state.current_quiz_state['timer_enabled'] = timer_enabled
                st.session_state.current_quiz_state['answers'] = []
                st.rerun()
            
            # 퀴즈 진행
            if st.session_state.current_quiz_state['start_time']:
                current_time = time.time()
                elapsed_time = current_time - st.session_state.current_quiz_state['start_time']
                
                # 타이머 표시
                if timer_enabled:
                    remaining_time = st.session_state.current_quiz_state['time_limit'] - elapsed_time
                    if remaining_time > 0:
                        mins, secs = divmod(int(remaining_time), 60)
                        st.markdown(f"⏰ **남은 시간: {mins:02d}:{secs:02d}**")
                    else:
                        st.error("⏰ 시간이 초과되었습니다!")
                        st.session_state.current_quiz_state['start_time'] = None
                        st.rerun()
                
                # 진행률 표시
                progress = st.progress(0)
                total_questions = len(exp['quiz']) + (1 if 'interactive_quiz' in exp else 0)
                
                # 객관식 퀴즈
                st.subheader("📝 객관식 퀴즈")
                score = 0
                answers = []
                
                for idx, item in enumerate(exp["quiz"]):
                    progress.progress((idx + 1) / total_questions)
                    
                    # 난이도 표시
                    difficulty_color = get_difficulty_color(item.get('difficulty', 'medium'))
                    st.markdown(f"""
                    <div style="border-left: 4px solid {difficulty_color}; padding-left: 10px; margin: 10px 0;">
                        <strong>Q{idx + 1}. {item['question']}</strong>
                        <br><small style="color: {difficulty_color};">
                        난이도: {item.get('difficulty', 'medium').upper()}</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    user_answer = st.radio(
                        "답을 선택하세요:",
                        item["options"],
                        key=f"q{quiz_experiment}_{idx}"
                    )
                    answers.append((user_answer, item["answer"], item["explanation"]))
                
                # 인터랙티브 퀴즈
                if 'interactive_quiz' in exp:
                    st.subheader("🎮 인터랙티브 퀴즈")
                    render_interactive_quiz(exp['interactive_quiz'], quiz_experiment)
                
                progress.progress(1.0)
                
                # 결과 확인
                if st.button("📊 결과 확인", key="check_results"):
                    # 점수 계산
                    for user, correct, _ in answers:
                        if user == correct:
                            score += 1
                    
                    percent = int(score / len(answers) * 100)
                    time_taken = int(elapsed_time)
                    
                    # 결과 저장
                    save_quiz_result(quiz_experiment, percent, time_taken, exp['difficulty'])
                    
                    # 결과 표시
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("점수", f"{percent}점")
                    with col2:
                        st.metric("소요 시간", f"{time_taken}초")
                    with col3:
                        st.metric("정답률", f"{score}/{len(answers)}")
                    
                    # 상세 결과
                    st.subheader("📋 상세 결과")
                    for idx, (user, correct, explanation) in enumerate(answers):
                        result = "🟢 정답" if user == correct else "🔴 오답"
                        with st.expander(f"Q{idx + 1}: {result}"):
                            st.write(f"**선택한 답:** {user}")
                            st.write(f"**정답:** {correct}")
                            st.write(f"**해설:** {explanation}")
                    
                    # 성취도 메시지
                    if percent >= 90:
                        st.success("🏆 완벽합니다! 이 실험의 마스터가 되셨습니다!")
                    elif percent >= 80:
                        st.success("🎉 훌륭합니다! 이 실험에 대한 이해도가 높습니다!")
                    elif percent >= 60:
                        st.info("📚 괜찮습니다! 조금 더 학습하면 완벽할 것 같습니다.")
                    else:
                        st.warning("💪 더 열심히! 기본 개념부터 다시 학습해보세요.")
                        # 약한 영역 추가
                        if quiz_experiment not in st.session_state.user_profile['weak_areas']:
                            st.session_state.user_profile['weak_areas'].append(quiz_experiment)
                    
                    # 퀴즈 상태 초기화
                    st.session_state.current_quiz_state['start_time'] = None
    
    with tab3:
        st.header("📈 학습 분석")
        
        if not st.session_state.user_profile['quiz_history']:
            st.info("아직 퀴즈 기록이 없습니다. 퀴즈를 먼저 풀어보세요!")
        else:
            # 전체 통계
            df = pd.DataFrame(st.session_state.user_profile['quiz_history'])
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("평균 점수", f"{df['score'].mean():.1f}점")
            with col2:
                st.metric("최고 점수", f"{df['score'].max()}점")
            with col3:
                st.metric("평균 시간", f"{df['time_taken'].mean():.1f}초")
            with col4:
                st.metric("총 학습 시간", f"{df['time_taken'].sum()//60}분")
            
            # 차트들
            col1, col2 = st.columns(2)
            
            with col1:
                # 진행률 차트
                progress_chart = create_progress_chart()
                if progress_chart:
                    st.plotly_chart(progress_chart, use_container_width=True)
            
            with col2:
                # 난이도별 분포
                difficulty_chart = create_difficulty_distribution()
                if difficulty_chart:
                    st.plotly_chart(difficulty_chart, use_container_width=True)
            
            # 실험별 성과 분석
            st.subheader("🔬 실험별 성과")
            exp_performance = df.groupby('experiment').agg({
                'score': ['mean', 'max', 'count'],
                'time_taken': 'mean'
            }).round(1)
            
            # 컬럼명 정리
            exp_performance.columns = ['평균 점수', '최고 점수', '시도 횟수', '평균 시간']
            st.dataframe(exp_performance)
            
            # 약한 영역 분석
            if st.session_state.user_profile['weak_areas']:
                st.subheader("💪 개선이 필요한 영역")
                for area in st.session_state.user_profile['weak_areas']:
                    st.warning(f"• {area}")
                    if st.button(f"{area} 다시 학습하기", key=f"retry_{area}"):
                        st.session_state.selected_experiment = area
                        st.rerun()
            
            # 학습 기록 상세
            st.subheader("📚 학습 기록")
            st.dataframe(df.sort_values('date', ascending=False))
    
    with tab4:
        st.header("⚙️ 설정")
        
        # 개인화 설정
        st.subheader("👤 개인화 설정")
        
        # 학습 목표 설정
        daily_goal = st.slider("일일 학습 목표 (퀴즈 수)", 1, 10, 3)
        
        # 알림 설정
        notifications = st.checkbox("학습 알림 받기", value=True)
        
        # 난이도 자동 조정
        auto_difficulty = st.checkbox("실력에 따른 난이도 자동 조정", value=False)
        
        # 데이터 관리
        st.subheader("📊 데이터 관리")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 학습 기록 다운로드"):
                if st.session_state.user_profile['quiz_history']:
                    df = pd.DataFrame(st.session_state.user_profile['quiz_history'])
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="CSV 다운로드",
                        data=csv,
                        file_name=f"quiz_history_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime='text/csv'
                    )
        
        with col2:
            if st.button("🗑️ 모든 기록 삭제"):
                if st.checkbox("정말 삭제하시겠습니까?"):
                    st.session_state.user_profile = {
                        'name': st.session_state.user_profile['name'],
                        'level': st.session_state.user_profile['level'],
                        'quiz_history': [],
                        'favorites': [],
                        'weak_areas': [],
                        'study_streak': 0,
                        'total_points': 0
                    }
                    st.success("모든 기록이 삭제되었습니다.")
                    st.rerun()
        
        # 앱 정보
        st.subheader("ℹ️ 앱 정보")
        st.markdown("""
        **🧪 랩 실습 퀴즈 학습기 v2.0**
        
        이 앱은 실험실 실습을 위한 종합 학습 도구입니다.
        
        **주요 기능:**
        - 📚 실험별 상세 학습 자료
        - 🎯 다양한 형태의 퀴즈 (객관식, 인터랙티브)
        - 📈 개인별 학습 진도 분석
        - ⏰ 타이머 기능
        - 👤 개인화된 학습 경험
        
        **지원 실험:**
        - STZ 주사액 제조
        - PCR (Polymerase Chain Reaction)
        - Cell Culture
        - Western Blot
        - ELISA
        - Flow Cytometry
        
        **개발자:** AI Assistant
        **버전:** 2.0
        """)

if __name__ == "__main__":
    main()
