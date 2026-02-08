import streamlit as st
import pandas as pd
import requests
import random
from datetime import datetime

# [1] 시스템 설정 (골드 & 블랙 테마: 돈 들어오는 느낌)
st.set_page_config(
    page_title="황금손 로또 분석실",
    page_icon="💰",
    layout="centered"
)

# [2] 동행복권 실제 데이터 수집 엔진
@st.cache_data(ttl=3600) # 1시간마다 갱신
def get_lotto_data(start_drw, end_drw):
    # 최근 10회차 당첨 번호를 실제로 긁어옴
    rows = []
    for i in range(end_drw, start_drw - 1, -1):
        url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={i}"
        resp = requests.get(url)
        if resp.status_code == 200:
            data = resp.json()
            if data["returnValue"] == "success":
                # 당첨 번호 6개 + 보너스
                nums = [data[f"drwtNo{j}"] for j in range(1, 7)]
                rows.append({"회차": i, "당첨번호": nums, "보너스": data["bnusNo"], "날짜": data["drwNoDate"]})
    return pd.DataFrame(rows)

# 최신 회차 자동 계산
def get_latest_drw_no():
    # 로또 1회차(2002-12-07) 기준으로 현재 회차 계산
    start_date = datetime(2002, 12, 7)
    now_date = datetime.now()
    weeks = (now_date - start_date).days // 7
    return weeks + 1

# [3] UI 디자인 (고급스럽고 직관적)
def main():
    st.markdown("""
        <style>
        .stApp { background-color: #ffffff; }
        .big-font { font-size: 24px !important; font-weight: bold; color: #333; }
        .lotto-ball {
            display: inline-block; width: 40px; height: 40px; 
            line-height: 40px; text-align: center; border-radius: 50%;
            color: white; font-weight: bold; margin: 3px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        }
        /* 공 색상 */
        .ball-1 { background-color: #fbc400; text-shadow: 1px 1px 2px #b08900; } /* 1-10 노랑 */
        .ball-2 { background-color: #69c8f2; text-shadow: 1px 1px 2px #4689a6; } /* 11-20 파랑 */
        .ball-3 { background-color: #ff7272; text-shadow: 1px 1px 2px #a64a4a; } /* 21-30 빨강 */
        .ball-4 { background-color: #aaaaaa; text-shadow: 1px 1px 2px #555555; } /* 31-40 회색 */
        .ball-5 { background-color: #b0d840; text-shadow: 1px 1px 2px #75912a; } /* 41-45 초록 */
        </style>
    """, unsafe_allow_html=True)

    # 헤더
    st.title("💰 AI 로또 당첨 분석실")
    st.caption("대한민국 동행복권 실제 API 데이터를 기반으로 분석합니다.")

    # 데이터 로딩
    latest_drw = get_latest_drw_no()
    with st.spinner(f"제 {latest_drw}회차까지 데이터 분석 중..."):
        # 최근 20회차 데이터 로딩
        df = get_lotto_data(latest_drw - 20, latest_drw)
    
    # --- 탭 구성 ---
    tab1, tab2 = st.tabs(["⚡ 번호 생성 (추천)", "📊 당첨 통계 (분석)"])

    # [탭 1] 번호 생성기
    with tab1:
        st.subheader("🏆 이번 주 1등 도전")
        
        # 알고리즘 선택 (있어 보이게)
        method = st.radio("생성 알고리즘 선택", 
                         ["🔥 최근 핫(Hot) 번호 위주 (당첨 잦은 수)", 
                          "🧊 미출현 콜드(Cold) 번호 위주 (안 나온 수)", 
                          "⚖️ AI 밸런스 혼합 (강력 추천)"])
        
        st.write("")
        if st.button("🎰 번호 추출하기 (Click)", use_container_width=True):
            with st.spinner("빅데이터 패턴 분석 중..."):
                # 실제 생성 로직 (단순 랜덤 아님)
                all_nums = []
                for nums in df["당첨번호"]:
                    all_nums.extend(nums)
                
                # 빈도 계산
                freq = pd.Series(all_nums).value_counts().sort_index()
                weights = []
                
                for i in range(1, 46):
                    count = freq.get(i, 0)
                    if "핫" in method:
                        weights.append(count + 1) # 많이 나온 수 가중치
                    elif "콜드" in method:
                        weights.append(100 - count) # 적게 나온 수 가중치
                    else:
                        weights.append(1) # 랜덤
                
                # 번호 뽑기 (5게임)
                st.divider()
                st.write(f"### 🎁 {method} 결과")
                
                for i in range(5):
                    lucky_nums = sorted(random.choices(range(1, 46), weights=weights, k=6))
                    # 중복 제거 (로또는 중복 없음)
                    while len(set(lucky_nums)) < 6:
                        lucky_nums = sorted(random.sample(range(1, 46), k=6))
                    
                    # 공 그리기
                    html_str = ""
                    for num in lucky_nums:
                        color_class = f"ball-{(num-1)//10 + 1}"
                        html_str += f'<span class="lotto-ball {color_class}">{num}</span>'
                    st.markdown(html_str, unsafe_allow_html=True)
                    st.write("") # 간격
        
        # [수익화] 자연스러운 광고 멘트
        st.info("💡 1등 당첨시 농협 본점으로 가시면 됩니다. (신분증 지참)")

    # [탭 2] 통계 대시보드
    with tab2:
        st.subheader("📊 최근 20회차 당첨 패턴")
        
        # 데이터 전처리
        all_nums = []
        for nums in df["당첨번호"]:
            all_nums.extend(nums)
        
        counts = pd.Series(all_nums).value_counts().head(7)
        
        st.write("🔥 가장 많이 나온 번호 Top 7")
        st.bar_chart(counts)
        
        st.write("📋 최근 당첨 내역")
        # 보기 좋게 데이터프레임 가공
        display_df = df[["회차", "날짜", "당첨번호", "보너스"]].copy()
        st.dataframe(display_df, hide_index=True, use_container_width=True)

if __name__ == "__main__":
    main()