import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

# [1] 시스템 설정 및 보안 (가이드 준수)
st.set_page_config(
    page_title="J-TECH Market Intelligence",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# [2] 고급 UI/UX 커스텀 (CSS) - 사이드바 버튼 디자인 통합
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
    
    /* 전체 배경 및 사이드바 통합 디자인 */
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    [data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #30363d;
    }
    
    /* 사이드바 접기 화살표 버튼 위치 및 색상 보정 */
    [data-testid="stSidebarNav"] + div { color: #58a6ff; }
    button[kind="header"] { background-color: transparent; color: #58a6ff; }

    /* 뉴스 카드 전문 디자인 */
    .news-wrapper {
        background-color: #1c2128;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #30363d;
        margin-bottom: 16px;
        transition: all 0.3s ease;
    }
    .news-wrapper:hover {
        border-color: #58a6ff;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .news-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #58a6ff;
        text-decoration: none;
        display: block;
        margin-bottom: 8px;
    }
    .news-tag {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 4px;
        background-color: #238636;
        color: white;
        font-size: 0.75rem;
        margin-right: 8px;
    }
    .news-date { color: #8b949e; font-size: 0.85rem; }

    /* 광고 슬롯 섹션 */
    .ad-slot {
        background: linear-gradient(135deg, #161b22 0%, #0d1117 100%);
        border: 1px dashed #484f58;
        border-radius: 10px;
        padding: 25px;
        text-align: center;
        color: #8b949e;
        margin: 20px 0;
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)

# [3] 데이터 엔진 (Google RSS 최적화)
@st.cache_data(ttl=600)
def fetch_industry_data(keyword):
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://news.google.com/rss/search?q={keyword}&hl=ko&gl=KR&ceid=KR:ko"
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'xml')
        items = soup.find_all('item')
        results = []
        for item in items[:12]:
            results.append({
                "title": item.title.text,
                "link": item.link.text,
                "date": item.pubDate.text[:16]
            })
        return pd.DataFrame(results)
    except Exception as e:
        return pd.DataFrame()

def main():
    # --- 사이드바 영역 ---
    with st.sidebar:
        st.markdown("<h2 style='color:#58a6ff;'>💎 J-TECH Control</h2>", unsafe_allow_html=True)
        st.write("전문 제조 지식 기반 시장 분석 시스템")
        st.divider()
        
        category = st.selectbox(
            "📍 모니터링 섹터 변경",
            ["원자재 & LME 시황", "글로벌 물류 & 공급망", "EV & 배터리 산업", "반도체 & IT 장비"]
        )
        
        st.divider()
        st.info("💡 Tip: 매일 오전 9시 지표가 갱신됩니다. 광고 문의는 하단 메일을 이용해 주세요.")
        st.caption("Admin: jtech1110@gmail.com")

    # --- 메인 컨텐츠 영역 ---
    col_t1, col_t2 = st.columns([3, 1])
    with col_t1:
        st.markdown(f"<h1 style='margin-bottom:0;'>📡 {category} 분석 터미널</h1>", unsafe_allow_html=True)
        st.write(f"최종 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # [수익화 포인트 1] 상단 광고 지점
    st.markdown('<div class="ad-slot">광고 배너 위치 (구글 애드센스 승인 대기 중)</div>', unsafe_allow_html=True)

    # 주요 지표 대시보드 (방문 유도용)
    st.subheader("📊 주요 시장 지표")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("LME 구리", "$9,415", "-0.8%")
    m2.metric("LME 알루미늄", "$2,482", "+1.2%")
    m3.metric("USD/KRW", "1,384.5", "▲ 2.1")
    m4.metric("KOSPI", "2,562.1", "▼ 15.4")

    st.divider()

    # 뉴스 엔진 구동
    keywords = {
        "원자재 & LME 시황": "구리 알루미늄 원자재 전망 시세",
        "글로벌 물류 & 공급망": "해운 운임 공급망 물류 대란",
        "EV & 배터리 산업": "전기차 배터리 리튬 니켈 소재",
        "반도체 & IT 장비": "반도체 수급 파운드리 장비 시장"
    }
    
    st.subheader("📰 실시간 산업 동향")
    news_df = fetch_industry_data(keywords[category])

    if not news_df.empty:
        # 뉴스 출력을 2열로 배치하여 가독성 증대
        n_col1, n_col2 = st.columns(2)
        for idx, row in news_df.iterrows():
            target_col = n_col1 if idx % 2 == 0 else n_col2
            with target_col:
                st.markdown(f"""
                <div class="news-wrapper">
                    <span class="news-tag">{category.split(' ')[0]}</span>
                    <a href="{row['link']}" target="_blank" class="news-title">{row['title']}</a>
                    <div class="news-date">🗓 {row['date']} | J-TECH 분석 엔진</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("현재 데이터를 불러올 수 없습니다. 잠시 후 다시 시도해주세요.")

    # [수익화 포인트 2] 하단 광고 지점
    st.markdown('<div class="ad-slot">관련 산업 추천 링크 광고 (AdSense)</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()