import streamlit as st
import pandas as pd

# [1] 시스템 설정 (와이드 모드: 데이터 많이 보여주기 위함)
st.set_page_config(
    page_title="J-TECH Parts Finder",
    page_icon="🔍",
    layout="wide"
)

# [2] 가짜 데이터베이스 (나중에 엑셀로 관리하면 됨)
# 현장에서 가장 많이 찾는 커넥터/터미널 예시 데이터
data = {
    "브랜드": ["MOLEX", "MOLEX", "JST", "JST", "YEONHO", "KET", "TE"],
    "시리즈": ["Mini-Fit Jr", "Micro-Fit", "PH", "XH", "SMH200", "090 II", "AMP Superseal"],
    "파트넘버(P/N)": ["5557-02R", "43025-0400", "PHR-2", "XHP-2", "SMH200-02", "MG610028", "282080-1"],
    "설명": ["4.2mm Pitch, 2 Circuit Receptacle", "3.0mm Pitch, 4 Circuit", "2.0mm Pitch Housing", "2.5mm Pitch Housing", "2.00mm Pitch", "Sealed Connector 2P", "1.5 Series Sealed"],
    "매칭 터미널": ["5556T", "43030", "SPH-002T", "SXH-001T", "YST200", "ST730644", "282110-1"],
    "피치(mm)": [4.2, 3.0, 2.0, 2.5, 2.0, 2.3, 6.0],
    "상태": ["재고 보유", "수급 불안", "재고 보유", "재고 보유", "발주 필요", "단종 예정", "재고 보유"]
}
df = pd.DataFrame(data)

def main():
    # 사이드바: 기능 전환
    with st.sidebar:
        st.title("J-TECH Solutions")
        mode = st.radio("메뉴 선택", ["🔍 부품 규격 검색", "⚙️ 현장 계산기 (구버전)"])
        st.info("💡 데이터베이스 업데이트: 2026.02.09")
        st.write("문의: jtech1110@gmail.com")

    if mode == "🔍 부품 규격 검색":
        # 메인 타이틀: 있어 보이는 검색 엔진 스타일
        st.markdown("""
        <h1 style='text-align: center; color: #333;'>⚡ J-TECH Cross-Reference</h1>
        <p style='text-align: center; color: #666;'>국내외 30,000개 이상의 하네스 부품 데이터베이스 (Demo)</p>
        """, unsafe_allow_html=True)

        st.write("---")

        # 검색창 (크고 아름답게)
        c1, c2, c3 = st.columns([1, 6, 1])
        with c2:
            search_query = st.text_input("파트넘버(P/N), 시리즈, 또는 브랜드 검색", placeholder="예: 5557, JST, 2.0mm")

        # [수익화 포인트] 검색 결과 상단 광고 영역
        st.markdown('<div style="background:#f0f2f6; padding:15px; text-align:center; border-radius:10px; color:#888; margin: 20px 0;">📢 AD: 커넥터 소량 구매는 OO전자 (클릭)</div>', unsafe_allow_html=True)

        # 검색 로직
        if search_query:
            # 대소문자 무시하고 검색
            mask = df.apply(lambda x: x.astype(str).str.contains(search_query, case=False).any(), axis=1)
            result_df = df[mask]
        else:
            result_df = df # 검색어 없으면 전체 보여줌 (혹은 숨김 가능)

        # 결과 테이블 보여주기
        if not result_df.empty:
            st.success(f"총 {len(result_df)}건의 부품이 검색되었습니다.")
            
            # 스트림릿 내장 데이터프레임 (정렬, 필터링, 전체화면 가능 - 프로페셔널함)
            st.dataframe(
                result_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "파트넘버(P/N)": st.column_config.TextColumn("Part Number", help="제조사 공식 파트넘버", width="medium"),
                    "매칭 터미널": st.column_config.TextColumn("Matching Terminal", help="호환되는 터미널 규격", width="medium"),
                    "상태": st.column_config.StatusColumn("Stock Status", help="현재 수급 상태")
                }
            )
        else:
            st.warning("검색 결과가 없습니다. 스펠링을 확인해주세요.")
            # 검색 결과 없을 때 보여줄 추천 상품 (이것도 광고)
            st.info("비슷한 규격의 대체품을 찾으시나요? [기술 상담 요청]")

    else:
        # 아까 만든 계산기 (도구함으로 이동)
        st.subheader("⚙️ 엔지니어링 도구 모음")
        tab1, tab2 = st.tabs(["AWG 변환", "절단 계산"])
        
        with tab1:
            st.write("AWG ↔ SQ 빠른 변환표")
            st.json({"AWG 24": "0.2sq", "AWG 22": "0.3sq", "AWG 20": "0.5sq"}) # 간단하게 표현
        
        with tab2:
            st.write("케이블 롤 소요량 계산")
            roll = st.number_input("롤 길이(m)", 300)
            cut = st.number_input("절단(mm)", 150)
            if cut > 0:
                st.metric("예상 수량", f"{int(roll*1000/cut):,} 개")

if __name__ == "__main__":
    main()