import streamlit as st
import pandas as pd
import itertools

# 1. 웹 페이지 기본 설정
st.set_page_config(page_title="윤정의 키워드 마스터", layout="wide")

st.title("🎯 네이버 플레이스 1만개 키워드 자동 생성기")
st.info("윤정님의 상권별 랜드마크 DB와 정솥밥 마케팅 로직이 탑재된 프로그램입니다.")

# 2. 상권별 기본 데이터베이스 (윤정님의 엑셀 데이터를 기반으로 구성)
# 컨설팅 시 이 상권 리스트를 늘려가면 가치가 높아집니다.
DB = {
    "역삼 (강남권)": ["강남역", "역삼역", "GFC", "센터필드", "GS타워", "차병원", "교대역", "삼성역", "지에스타워", "신세계강남", "국기원"],
    "한남 (용산권)": ["나인원한남", "유엔빌리지", "순천향대병원", "블루스퀘어", "리움미술관", "이태원", "용산역", "몬드리안서울", "하얏트호텔"],
    "수원 (행궁동)": ["화성행궁", "수원역", "행리단길", "통닭거리", "수원시청", "팔달문", "장안문", "수원월드컵경기장", "인계동"],
    "마곡 (강서권)": ["마곡나루역", "마곡역", "서울식물원", "LG아트센터", "발산역", "코엑스마곡", "메이필드호텔", "강서구청"]
}

# 3. 마케팅 수식어 및 메뉴 로직 (윤정님의 ALL 테마 및 메뉴 파일 기준)
themes = ["가성비", "청첩장모임", "분위기좋은", "회식하기좋은", "내돈내산", "찐맛집", "부모님식사", "데이트코스", "조용한", "룸있는"]
menus = ["솥밥", "스테이크솥밥", "장어솥밥", "한정식", "점심", "저녁", "히츠마부시", "룸식당", "반상", "한상"]
suffixes = ["맛집", "추천", "식당", "추천맛집", "추천식당", "점심맛집", "저녁맛집"]

# 4. 웹 화면 입력 섹션
with st.sidebar:
    st.header("⚙️ 상권 설정")
    selected_area = st.selectbox("분석할 상권 선택", list(DB.keys()))
    
    st.write("---")
    st.write("직접 입력도 가능합니다.")
    custom_locs = st.text_area("추가 랜드마크 (한 줄에 하나씩)", "")

# 5. 메인 조합 화면
st.subheader(f"📍 {selected_area} 키워드 조합 설정")

col1, col2, col3 = st.columns(3)

with col1:
    # 선택된 상권의 기본 랜드마크 + 직접 입력한 랜드마크 합치기
    base_locs = DB[selected_area]
    added_locs = [x.strip() for x in custom_locs.split('\n') if x.strip()]
    final_locs = st.multiselect("사용할 장소/랜드마크", base_locs + added_locs, default=base_locs)

with col2:
    selected_themes = st.multiselect("적용할 마케팅 테마", themes, default=themes[:6])

with col3:
    selected_menus = st.multiselect("대표 메뉴/업종", menus, default=menus[:5])

# 6. 키워드 생성 및 다운로드 로직
st.write("---")
if st.button("🚀 키워드 조합 생성 시작 (최대 10,000개)"):
    # 모든 경우의 수 조합 (Cartesian Product)
    combos = list(itertools.product(final_locs, selected_themes, selected_menus, suffixes))
    
    # 네이버 광고 가이드에 따른 정제 (중복 제거 및 25자 제한)
    results = []
    for c in combos:
        kw = f"{c[0]} {c[1]} {c[2]} {c[3]}"
        if len(kw) <= 25:
            results.append(kw)
    
    # 중복 제거
    results = list(set(results))
    
    # 결과 출력
    df = pd.DataFrame(results, columns=["네이버 플레이스 광고 키워드"])
    st.success(f"성공! 총 {len(df):,}개의 유효 키워드가 생성되었습니다.")
    
    # 샘플 보여주기
    st.dataframe(df.head(100), use_container_width=True)
    
    # 엑셀(CSV) 다운로드 버튼
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📊 생성된 키워드 엑셀 파일로 받기",
        data=csv,
        file_name=f"naver_keywords_{selected_area}.csv",
        mime="text/csv",
    )
