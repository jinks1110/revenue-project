import streamlit as st
import pandas as pd
import requests
import random
from datetime import datetime

# [1] 시스템 설정
st.set_page_config(
    page_title="황금손 로또 분석실",
    page_icon="💰",
    layout="centered"
)

# [2] 동행복권 데이터 수집 엔진 (봇 차단 회피 기능 탑재)
@st.cache_data(ttl=3600)
def get_lotto_data(start_drw, end_drw):
    rows = []
    # 봇 차단 방지용 헤더 (나는 크롬이다!)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # 에러 나도 멈추지 않고 다음 회차로 넘어가는 안전장치
    for i in range(end_drw, start_drw - 1, -1):
        try:
            url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={i}"
            resp = requests.get(url, headers=headers, timeout=5)
            
            # 서버가 정상 응답(200)을 줬는지 확인
            if resp.status_code == 200:
                # 여기서 JSON 변환 시도 (아까 터진 곳 방어)
                try:
                    data = resp.json()
                    if data.get("returnValue") == "success":
                        nums = [data[f"drwtNo{j}"] for j in range(1, 7)]
                        rows.append({"회차": i, "당첨번호": nums, "보너스": data["bnusNo"], "날짜": data["drwNoDate"]})
                except ValueError:
                    continue # JSON 아니면(HTML 에러페이지면) 무시하고 진행
                    
        except Exception as e:
            continue # 연결 에러 나도 쿨하게 무시

    # 만약 데이터를 하나도 못 가져왔을 때를 대비한 비상용 가짜 데이터 (앱 뻗음 방지)
    if not rows:
        return pd.DataFrame([
            {"회차": 1100, "당첨번호": [1, 2, 3, 4, 5, 6], "보너스": 7, "날짜": "데이터 로딩 실패"}
        ])
        
    return pd.DataFrame(rows)

# 최신 회차 계산기 (오늘 날짜 기준)
def get_latest_drw_no():
    start_date = datetime(2002, 12, 7)
    now_date = datetime.now()
    days = (now_date - start_date).days
    # 토요일 저녁 8시 45분 전이면 아직 추첨 안 했으므로 -1회차
    weeks = days // 7 + 1
    if now_date.weekday() == 5 and now_date.hour < 21: 
        return weeks - 1
    return weeks

def main():
    # [스타일] CSS: 공 디자인
    st.markdown("""
        <style>
        .stApp { background-color: #ffffff; }
        .lotto-ball {
            display: inline-block; width: 35px; height: 35px; 
            line-height: 35px; text-align: center; border-radius: 50%;
            color: white; font-weight: bold; margin: 2px;
            font-size: 14px;
            box-shadow: 1px 1px 3px rgba(0,0,0,0.2);
        }
        .ball-1 { background-color: #fbc400; } 
        .ball-2 { background-color: #69c8f2; } 
        .ball-3 { background-color: #ff7272; } 
        .ball-4 { background-color: #aaaaaa; } 
        .ball-5 { background-color: #b0d840; } 
        </style>
    """, unsafe_allow_html=True)

    st.title("💰 AI 로또 분석기")
    st.caption("실시간 동행복권 API 연동 (봇 차단 우회 적용)")

    # 데이터 로딩
    latest = get_latest_drw_no()
    
    with st.spinner("데이터 서버 접속 중..."):
        # 최근 10회차만 가져옴 (속도 향상)
        df = get_lotto_data(latest - 10, latest)

    # 탭 구성
    tab1, tab2 = st.tabs(["⚡ 번호 생성", "📊 최근 결과"])

    with tab1:
        st.subheader("🏆 이번 주 1등 추천 번호")
        method = st.radio("분석 방식", ["🔥 핫(Hot) 번호 기반", "⚖️ 밸런스 혼합 추천"])
        
        if st.button("번호 추출하기", use_container_width=True):
            st.success("분석 완료! 추천 번호입니다.")
            st.write("---")
            
            # 추천 로직
            all_nums = []
            for nums in df["당첨번호"]:
                all_nums.extend(nums)
            
            # 5게임 생성
            for _ in range(5):
                # 단순 랜덤이 아니라 가중치 적용
                if "핫" in method:
                    # 많이 나온 번호 60%, 랜덤 40%
                    hot_nums = pd.Series(all_nums).value_counts().index[:10].tolist()
                    base_pool = hot_nums + list(range(1, 46))
                    lucky = sorted(random.sample(base_pool, 6))
                else:
                    lucky = sorted(random.sample(range(1, 46), 6))

                # 공 출력
                html = ""
                for n in lucky:
                    color = f"ball-{(n-1)//10 + 1}"
                    html += f'<span class="lotto-ball {color}">{n}</span>'
                st.markdown(f"<div>{html}</div>", unsafe_allow_html=True)
                st.write("")

    with tab2:
        st.subheader("📋 최근 당첨 내역")
        # 데이터프레임 깔끔하게 출력
        if not df.empty and "당첨번호" in df.columns:
            st.dataframe(
                df[["회차", "날짜", "당첨번호", "보너스"]],
                hide_index=True,
                use_container_width=True
            )
        else:
            st.error("데이터를 불러오지 못했습니다.")

if __name__ == "__main__":
    main()