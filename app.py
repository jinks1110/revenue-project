import streamlit as st

# [1] 기본 설정: 순정 화이트 모드 (가독성 최우선)
st.set_page_config(
    page_title="J-Tech 현장 계산기",
    page_icon="🔧",
    layout="centered"
)

# [데이터] AWG 규격 및 허용 전류 데이터 (일반적인 HIV/IV 기준 참고치)
wire_data = {
    "AWG 30": {"sq": "0.05", "amp": "불가"},
    "AWG 28": {"sq": "0.08", "amp": "0.5 A"},
    "AWG 26": {"sq": "0.13", "amp": "1.5 A"},
    "AWG 24": {"sq": "0.20", "amp": "2.5 A"},
    "AWG 22": {"sq": "0.30", "amp": "5 A"},
    "AWG 20": {"sq": "0.50", "amp": "9 A"},
    "AWG 18": {"sq": "0.75", "amp": "13 A"},
    "AWG 16": {"sq": "1.25", "amp": "19 A"},
    "AWG 14": {"sq": "2.0",  "amp": "27 A"},
    "AWG 12": {"sq": "3.5",  "amp": "37 A"},
    "AWG 10": {"sq": "5.5",  "amp": "49 A"},
    "AWG 8":  {"sq": "8.0",  "amp": "61 A"}
}

def main():
    st.title("🔧 제이테크 실무 도구 모음")
    
    # 상단 탭으로 기능 3개 깔끔하게 분리
    tab1, tab2, tab3 = st.tabs(["📏 규격 변환", "✂️ 절단 수량 계산", "⚡ 허용 전류"])

    # --- 기능 1: AWG 변환기 ---
    with tab1:
        st.subheader("AWG ↔ SQ 변환")
        selected_awg = st.selectbox("AWG 사이즈 선택", list(wire_data.keys()))
        
        sq_val = wire_data[selected_awg]["sq"]
        
        st.write("---")
        # 결과를 아주 크게 보여줌
        st.metric(label="변환 결과", value=f"{sq_val} SQ")
        st.caption("※ 제조사별 피복 두께에 따라 미세한 차이가 있을 수 있습니다.")

    # --- 기능 2: 절단 수량 계산기 (작업 지시용) ---
    with tab2:
        st.subheader("롤(Roll) 작업 수량 계산")
        
        c1, c2 = st.columns(2)
        with c1:
            roll_len = st.number_input("전선 한 롤 길이 (m)", value=300)
        with c2:
            cut_len = st.number_input("절단 길이 (mm)", value=150)
            
        margin_len = st.number_input("양끝 탈피 여유분 (mm/개당)", value=0)
        
        if cut_len > 0:
            # 계산 로직: (롤길이 * 1000) / (절단길이 + 여유분)
            total_len_mm = roll_len * 1000
            one_piece_len = cut_len + margin_len
            result_count = int(total_len_mm / one_piece_len)
            
            st.write("---")
            st.metric(label="생산 가능 수량", value=f"{result_count:,} 개")
            st.info(f"한 롤({roll_len}m)을 다 찍으면 약 {result_count}개 나옵니다.")

    # --- 기능 3: 허용 전류 확인 (안전 기준) ---
    with tab3:
        st.subheader("전선별 허용 전류표")
        st.write("설계할 때 참고하세요 (단선 기준 근사치)")
        
        # 보기 편하게 데이터프레임 대신 딕셔너리 리스트로 출력
        for awg, info in wire_data.items():
            with st.expander(f"{awg} ({info['sq']} SQ)"):
                st.write(f"### 💡 허용 전류: 약 {info['amp']}")
                st.write("※ 주위 온도 및 전선 가닥수에 따라 감소할 수 있음")

if __name__ == "__main__":
    main()