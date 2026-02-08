import streamlit as st

# [1] 페이지 설정 (꽉 찬 화면, 깔끔한 아이콘)
st.set_page_config(
    page_title="Future Vision | AI Solution",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# [2] 디자인 커스텀 (CSS) - 스트림릿 티 안 나게 만들기
st.markdown("""
    <style>
    /* 상단 헤더 숨기기 */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 전체 폰트 및 배경 */
    .stApp {
        background-color: #ffffff;
        color: #111111;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* 히어로 섹션 (메인 타이틀) 스타일 */
    .hero-title {
        font-size: 4.5rem;
        font-weight: 900;
        line-height: 1.2;
        background: -webkit-linear-gradient(45deg, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .hero-subtitle {
        font-size: 1.5rem;
        color: #6b7280;
        margin-bottom: 30px;
    }
    
    /* 카드 디자인 */
    .feature-card {
        background-color: #f9fafb;
        border-radius: 15px;
        padding: 30px;
        border: 1px solid #e5e7eb;
        transition: 0.3s;
        height: 100%;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        border-color: #3b82f6;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    # --- 1. 히어로 섹션 (메인 간판) ---
    c1, c2 = st.columns([1.2, 1])
    
    with c1:
        st.write("##") # 여백
        st.write("##")
        st.markdown('<p class="hero-title">NEXT LEVEL<br>DIGITAL EXPERIENCE</p>', unsafe_allow_html=True)
        st.markdown('<p class="hero-subtitle">우리는 기술의 한계를 넘어 새로운 가능성을 창조합니다.<br>당신의 비즈니스를 위한 완벽한 솔루션을 만나보세요.</p>', unsafe_allow_html=True)
        
        # 버튼 그룹
        b1, b2, _ = st.columns([1, 1, 2])
        with b1:
            st.button("🚀 시작하기", type="primary", use_container_width=True)
        with b2:
            st.button("문의하기", use_container_width=True)

    with c2:
        # 그럴싸한 랜덤 IT 이미지 (Unsplash 소스)
        st.image("https://images.unsplash.com/photo-1550751827-4bd374c3f58b?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80", use_column_width=True)

    st.write("---")

    # --- 2. 주요 기능 소개 (3단 레이아웃) ---
    st.markdown("<h2 style='text-align: center; margin-bottom: 50px;'>Why Choose Us?</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color:#3b82f6;">⚡ Ultra Fast</h3>
            <p style="color:#4b5563;">
                최신 클라우드 기술을 기반으로<br>
                압도적인 처리 속도를 경험하세요.<br>
                지연 없는 실시간 데이터 처리.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color:#8b5cf6;">🛡️ Secure & Safe</h3>
            <p style="color:#4b5563;">
                군사 등급의 암호화 기술로<br>
                당신의 소중한 데이터를 보호합니다.<br>
                24시간 보안 모니터링 시스템.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color:#ec4899;">💡 Smart AI</h3>
            <p style="color:#4b5563;">
                자체 개발한 인공지능 알고리즘이<br>
                복잡한 업무를 자동으로 처리합니다.<br>
                효율성을 극대화하세요.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.write("##")
    st.write("##")

    # --- 3. 신뢰도 지표 (숫자 강조) ---
    st.markdown("<h3 style='text-align: center; color: #6b7280;'>TRUSTED BY INNOVATORS</h3>", unsafe_allow_html=True)
    st.write("##")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(label="Active Users", value="120K+", delta="12%")
    m2.metric(label="Countries", value="54", delta="Global")
    m3.metric(label="Uptime", value="99.9%", delta="Stable")
    m4.metric(label="Support", value="24/7", delta="Live")

    st.write("---")

    # --- 4. 하단 푸터 ---
    f1, f2 = st.columns([3, 1])
    with f1:
        st.markdown("### Future Vision Inc.")
        st.caption("Seoul, Republic of Korea | contact@futurevision.com")
        st.caption("© 2026 Future Vision Inc. All rights reserved.")
    with f2:
        st.selectbox("Language", ["Korean", "English", "Japanese"])

if __name__ == "__main__":
    main()