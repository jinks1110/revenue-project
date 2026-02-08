import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# [1] 시스템 설정
st.set_page_config(
    page_title="J-TECH Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# [2] 가독성 끝판왕 스타일 (흰색/노란색 강조)
st.markdown("""
    <style>
    /* 배경은 어둡게, 하지만 글자는 무조건 흰색/밝은색 */
    .stApp { background-color: #000000 !important; color: #ffffff !important; }
    
    /* 사이드바 글자색 강제 고정 */
    [data-testid="stSidebar"] { background-color: #111111 !important; border-right: 1px solid #444; }
    [data-testid="stSidebar"] .stMarkdown p, label { color: #ffffff !important; font-weight: bold !important; font-size: 1.1rem !important; }

    /* 뉴스 카드: 제목을 형광 파랑/노랑 수준으로 밝게 */
    .news-box {
        background-color: #1a1a1a;
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #333;
        margin-bottom: 20px;
    }
    .news-title {
        color: #00ffff !important; /* 형광 하늘색: 가장 잘 보임 */
        font-size: 1.4rem !important;
        font-weight: 800 !important;
        text-decoration: none !important;
        line-height: 1.6;
    }
    .news-date { color: #ffff00 !important; font-size: 1rem; margin-top: 10px; font-weight: bold; } /* 노란색 날짜 */
    
    /* 지표 숫자 크고 밝게 */
    [data-testid="stMetricValue"] { color: #ffffff !important; font-size: 2.5rem !important; font-weight: 900 !important; }
    [data-testid="stMetricLabel"] { color: #aaaaaa !important; font-size: 1.2rem !important; }
    </style>
    """, unsafe_allow_html=True)

# [3] 뉴스 수집 엔진 (더 단순하고 강력하게)
@st.cache_data(ttl=60) # 1분마다 갱신해서 실시간성 확보
def fetch_news_simple(keyword):
    # RSS 대신 검색 결과에서 직접 긁는 방식으로 안정성 강화
    url = f"https://www.google.com/search?q={keyword}&tbm=nws&hl=ko"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # 구글 뉴스 검색 결과 파싱
        news_list = []
        # 최신 구글 뉴스 레이아웃에 맞춘 파싱 (안되면 기본 RSS로 자동 전환)
        items = soup.select('div.So06bc') or soup.select('div.g')
        
        for item in items[:10]:
            title_tag = item.select_one('div[role="heading"]') or item.select_one('h3')
            link_tag = item.find('a')
            if title_tag and link_tag:
                news_list.append({
                    "title": title_tag.get_text(),
                    "link": link_tag['href'],
                    "date": "최신 뉴스"
                })
        
        # 만약 긁어오기 실패하면 비상용 RSS 가동
        if not news_list:
            rss_url = f"https://news.google.com/rss/search?q={keyword}&hl=ko&gl=KR&ceid=KR:ko"
            r_rss = requests.get(rss_url, timeout=10)
            soup_rss = BeautifulSoup(r_rss.text, 'xml')
            for item in soup_rss.find_all('item')[:10]:
                news_list.append({
                    "title": item.title.text,
                    "link": item.link.text,
                    "date": item.pubDate.text[:16]
                })
        return pd.DataFrame(news_list)
    except:
        return pd.DataFrame()

def main():
    # --- 사이드바 ---
    with st.sidebar:
        st.markdown("<h1 style='color:white;'>📡 제이테크 모니터</h1>", unsafe_allow_html=True)
        category = st.radio("카테고리 선택", ["구리 원자재", "글로벌 환율", "반도체 공급망"])
        st.write("---")
        st.write(f"접속 시간: {datetime.now().strftime('%H:%M:%S')}")

    # --- 메인 영역 ---
    st.markdown(f"<h1 style='color: white; font-size: 3rem;'>📊 {category} 보고서</h1>", unsafe_allow_html=True)

    # 지표 숫자 (무조건 크게)
    c1, c2, c3 = st.columns(3)
    if "구리" in category:
        c1.metric("LME COPPER", "$9,415", "-0.8%")
        c2.metric("원/달러 환율", "1,384.5", "▲ 2.1")
        c3.metric("유가(WTI)", "$76.12", "▼ 0.5%")
    else:
        c1.metric("KOSPI", "2,560.1", "▼ 12.4")
        c2.metric("NASDAQ", "15,820", "+0.4%")
        c3.metric("금 시세", "$2,042", "+0.2%")

    st.write("---")
    
    # 뉴스 리스트
    df = fetch_news_simple(category)
    if not df.empty:
        for idx, row in df.iterrows():
            st.markdown(f"""
                <div class="news-box">
                    <a href="{row['link']}" target="_blank" class="news-title">{row['title']}</a>
                    <div class="news-date">🗓 {row['date']} | 관련 소식 보기</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.error("❌ 현재 뉴스를 불러오는 엔진에 오류가 있습니다. 잠시 후 다시 시도하세요.")

if __name__ == "__main__":
    main()