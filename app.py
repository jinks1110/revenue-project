import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# [시스템 설정]
st.set_page_config(
    page_title="J-Tech Control Tower v1.1", 
    page_icon="🏭", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# [스타일링]
st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #f0f2f6;
        border: 1px solid #d1d5db;
    }
    div.stButton > button:hover {
        border-color: #4CAF50;
        color: #4CAF50;
    }
    .news-card {
        padding: 15px;
        background-color: #ffffff;
        border-radius: 8px;
        margin-bottom: 10px;
        border-left: 5px solid #4CAF50;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# [핵심 로직] 아까 성공했던 '그 로직' 복구 + 에러 추적 기능 추가
@st.cache_data(ttl=300)
def fetch_news_rss(keyword):
    url = f"https://news.google.com/rss/search?q={keyword}&hl=ko&gl=KR&ceid=KR:ko"
    # 차단 방지용 헤더 추가
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        resp = requests.get(url, headers=headers, timeout=10) # 타임아웃 10초로 늘림
        soup = BeautifulSoup(resp.text, 'html.parser')
        items = soup.find_all('item')
        
        data = []
        for item in items[:8]: 
            title = item.find('title').get_text()
            
            # [복구된 로직] 안전하게 링크 추출
            link = ""
            try:
                if item.find('link'):
                    link = item.find('link').next_sibling
                    if link:
                        link = link.strip()
                    else:
                        link = item.find('link').get_text()
                
                # 비상용: 텍스트로 강제 추출
                if not link:
                    link = str(item).split('<link>')[1].split('</link>')[0]
            except:
                pass # 링크 추출 실패해도 제목은 보여주기 위함

            pubDate = item.find('pubDate').get_text() if item.find('pubDate') else ""
            
            # 날짜 포맷 깔끔하게 정리 (예: Mon, 07 Feb 2026 -> 2026-02-07)
            clean_date = pubDate[:16] 

            data.append({"Title": title, "Link": link, "Date": clean_date})
            
        return pd.DataFrame(data)
        
    except Exception as e:
        # 여기가 핵심: 에러가 나면 숨기지 말고 화면에 출력
        return str(e)

def main():
    # [사이드바]
    with st.sidebar:
        st.header("⚡ 빠른 감시")
        
        if 'target_keyword' not in st.session_state:
            st.session_state.target_keyword = "구리 시세"

        c1, c2 = st.columns(2)
        if c1.button("구리 (LME)"): st.session_state.target_keyword = "LME 구리 시세"
        if c2.button("환율 (USD)"): st.session_state.target_keyword = "원달러 환율"
        
        st.divider()
        st.session_state.target_keyword = st.text_input("직접 검색", value=st.session_state.target_keyword)

    # [메인 화면]
    st.title(f"📊 {st.session_state.target_keyword} 모니터링")
    st.markdown("---")

    # 뉴스 섹션
    st.subheader("📰 실시간 뉴스")
    
    with st.spinner("데이터 분석 중..."):
        result = fetch_news_rss(st.session_state.target_keyword)
        
        # 결과가 데이터프레임이면 성공, 문자열이면 에러 메시지
        if isinstance(result, pd.DataFrame):
            if not result.empty:
                # 2단 배열
                col1, col2 = st.columns(2)
                for idx, row in result.iterrows():
                    target_col = col1 if idx % 2 == 0 else col2
                    with target_col:
                        # HTML/CSS로 카드 디자인 적용
                        st.markdown(f"""
                        <div class="news-card">
                            <div style="font-weight:bold; font-size:1.1em; margin-bottom:5px;">
                                <a href="{row['Link']}" target="_blank" style="text-decoration:none; color:black;">
                                    {row['Title']}
                                </a>
                            </div>
                            <div style="color:grey; font-size:0.8em;">
                                🕒 {row['Date']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("검색 결과가 없습니다. (키워드를 바꿔보세요)")
        else:
            # 에러 발생 시 빨간 박스로 원인 출력
            st.error(f"⚠️ 시스템 오류 발생: {result}")
            st.info("해결책: 잠시 후 다시 시도하거나, 인터넷 연결을 확인하세요.")

if __name__ == "__main__":
    main()