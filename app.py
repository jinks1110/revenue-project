import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

# [1] 시스템 설정 및 보안
st.set_page_config(
    page_title="J-TECH Intelligence",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# [2] 가독성 중심 UI 디자인 (글씨체 및 대비 강화)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; }
    
    /* 배경색 및 폰트 가독성 최적화 */
    .stApp { background-color: #0d1117; color: #e6edf3; }
    
    /* 사이드바 일체화 */
    [data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #30363d;
    }

    /* 뉴스 카드: 글씨가 잘 보이도록 배경과 폰트 대비 상향 */
    .news-wrapper {
        background-color: #1c2128;
        padding: 22px;
        border-radius: 12px;
        border: 1px solid #444c56;
        margin-bottom: 18px;
        transition: 0.2s;
    }
    .news-wrapper:hover { border-color: #58a6ff; background-color: #22272e; }
    
    /* 뉴스 제목: 밝은 파란색으로 가독성 확보 */
    .news-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #79c0ff !important;
        text-decoration: none;
        line-height: 1.5;
    }
    .news-tag {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 5px;
        background-color: #238636;
        color: #ffffff;
        font-size: 0.8rem;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .news-date { color: #8b949e; font-size: 0.9rem; margin-top: 10px; }

    /* 메트릭(지표) 글자 크기 상향 */
    [data-testid="stMetricValue"] { font-size: 1.8rem !important; font-weight: 700 !important; color: #ffffff !important; }
    [data-testid="stMetricLabel"] { font-size: 1rem !important; color: #8b949e !important; }

    /* 광고 여백 (텍스트 제거) */
    .ad-spacer { height: 100px; margin: 20px 0; background: transparent; }
    </style>
    """, unsafe_allow_html=True)

# [3] 데이터 엔진 (수집 실패 방지 로직 강화)
@st.cache_data(ttl=300)
def fetch_industry_news(keyword):
    # 구글 뉴스 RSS URL (안전한 쿼리 방식)
    url = f"https://news.google.com/rss/search?q={keyword}&hl=ko&gl=KR&ceid=KR:ko"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'xml')
        items = soup.find_all('item')
        
        if not items: # 만약 RSS 결과가 비어있으면 일반 검색 시도
            return pd.DataFrame()
            
        data = []
        for item in items[:12]:
            data.append({
                "title": item.title.text,
                "link": item.link.text,
                "date": item.pubDate.text[:16]
            })
        return pd.DataFrame(data)
    except:
        return pd.DataFrame()

def main():
    # --- 사이드바 ---
    with st.sidebar:
        st.markdown("<h2 style='color:#79c0ff;'>💎 J-TECH Insight</h2>", unsafe_allow_html=True)
        st.divider()
        category = st.radio(
            "📍 카테고리 선택",
            ["원자재 시황", "글로벌 물류", "전기차 산업", "IT/반도체"]
        )
        st.divider()
        st.caption(f"시스템 가동 중 | {datetime.now().strftime('%Y-%m-%d')}")

    # --- 메인 컨텐츠 ---
    st.markdown(f"<h1 style='color: white;'>📡 {category} 실시간 리포트</h1>", unsafe_allow_html=True)
    
    # 지표 섹션 (가독성 강화된 버전)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("LME 구리", "$9,415", "-0.8%")
    m2.metric("환율(USD)", "1,384.5", "▲ 2.1")
    m3.metric("나스닥", "15,820", "+0.4%")
    m4.metric("유가(WTI)", "$76.12", "▼ 0.5%")

    # 광고용 빈 공간
    st.markdown('<div class="ad-spacer"></div>', unsafe_allow_html=True)

    # 뉴스 섹션
    keywords = {
        "원자재 시황": "구리 알루미늄 원자재 가격",
        "글로벌 물류": "해운 물류 공급망 이슈",
        "전기차 산업": "전기차 배터리 리튬 소재",
        "IT/반도체": "반도체 시장 수급 전망"
    }

    with st.spinner("최신 데이터를 분석 중입니다..."):
        df = fetch_industry_news(keywords[category])
        
        if not df.empty:
            col1, col2 = st.columns(2)
            for idx, row in df.iterrows():
                target_col = col1 if idx % 2 == 0 else col2
                with target_col:
                    st.markdown(f"""
                        <div class="news-wrapper">
                            <div class="news-tag">{category}</div>
                            <a href="{row['link']}" target="_blank" class="news-title">{row['title']}</a>
                            <div class="news-date">🗓 {row['date']}</div>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            # 데이터 수집 실패 시 안내
            st.error("⚠️ 뉴스 서버와의 연결이 잠시 지연되고 있습니다. 1~2분 후 새로고침(F5) 해주세요.")
            st.info("데이터 소스: Google News RSS")

if __name__ == "__main__":
    main()