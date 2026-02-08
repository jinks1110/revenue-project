import streamlit as st
import pandas as pd

# [1] 시스템 설정 (가독성 최우선 화이트 모드)
st.set_page_config(
    page_title="J-TECH 통합 솔루션",
    page_icon="🏭",
    layout="wide"
)

# [2] 데이터베이스 (부품 DB + AWG 규격)
# 부품 데이터 (예시)
parts_data = {
    "브랜드": ["MOLEX", "MOLEX", "JST", "JST", "YEONHO", "KET", "TE"],
    "시리즈": ["Mini-Fit Jr", "Micro-Fit", "PH", "XH", "SMH200", "090 II", "AMP Superseal"],
    "파트넘버": ["5557-02R", "43025-0400", "PHR-2", "XHP-2", "SMH200-02", "MG610028", "282080-1"],
    "설명": ["4.2mm Pitch 2P", "3.0mm Pitch 4P", "2.0mm Pitch 2P", "2.5mm Pitch 2P", "2.00mm Pitch", "Sealed 2P", "1.5 Series Sealed"],
    "매칭터미널": ["5556T", "43030", "SPH-002T", "SXH-001T", "YST200", "ST730644", "282110-1"],
    "재고상태": ["보유", "부족", "보유", "보유", "발주필요", "단종", "보유"]
}
df_parts = pd.DataFrame(parts_data)

# AWG 데이터 (복구됨)
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
    st.title("🏭 J-TECH 현장 통합 시스템")
    st.write("부품 검색부터 작업 계산까지 한 번에 해결하세요.")

    # [핵심] 기능 통합: 탭으로 '검색'과 '계산기'를 분리하여 둘 다 유지
    tab_search, tab_calc = st.tabs(["🔍 부품 규격 검색", "⚙️ 현장 계산기 (복구됨)"])

    # --- 탭 1: 부품 검색 엔진 (신규 아이디어) ---
    with tab_search:
        st.subheader("⚡ 하네스 부품 Cross-Reference")
        
        c1, c2 = st.columns([3, 1])
        with c1:
            search_query = st.text_input("부품명/시리즈 검색", placeholder="예: 5557, PHR, MOLEX")
        with c2:
            st.write("") 
            st.write("")
            st.button("검색") # 엔터 쳐도 되지만 버튼도 배치

        # [광고 영역] 자연스러운 배치
        st.info("📢 [광고] 커넥터 소량/샘플 구매는 '제이테크 스토어' (준비중)")

        # 검색 로직 (에러 방지를 위해 단순화)
        if search_query:
            mask = df_parts.apply(lambda x: x.astype(str).str.contains(search_query, case=False).any(), axis=1)
            result_df = df_parts[mask]
        else:
            result_df = df_parts

        # 결과 출력 (에러 원인이었던 column_config 제거 -> 기본 표로 변경)
        if not result_df.empty:
            st.dataframe(result_df, use_container_width=True, hide_index=True)
        else:
            st.warning("검색 결과가 없습니다.")

    # --- 탭 2: 현장 계산기 (삭제된 기능 완벽 복구) ---
    with tab_calc:
        st.subheader("🔧 엔지니어링 실무 도구")
        
        # 내부 탭으로 3가지 기능 정리
        sub_tab1, sub_tab2, sub_tab3 = st.tabs(["📏 AWG 변환", "✂️ 롤 절단 계산", "⚡ 허용 전류"])

        # 1. AWG 변환
        with sub_tab1:
            col1, col2 = st.columns(2)
            with col1:
                selected_awg = st.selectbox("AWG 선택", list(wire_data.keys()))
            with col2:
                st.metric("변환 결과", f"{wire_data[selected_awg]['sq']} SQ")

        # 2. 롤 절단 계산
        with sub_tab2:
            c1, c2 = st.columns(2)
            roll_len = c1.number_input("롤 길이 (m)", value=300)
            cut_len = c2.number_input("절단 길이 (mm)", value=150)
            if cut_len > 0:
                count = int((roll_len * 1000) / cut_len)
                st.metric("생산 가능 수량", f"{count:,} 개")

        # 3. 허용 전류표
        with sub_tab3:
            st.write("규격별 허용 전류 (참고치)")
            st.table(pd.DataFrame(wire_data).T[['amp']])

if __name__ == "__main__":
    main()