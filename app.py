import streamlit as st
import pandas as pd
import itertools

# 1. 웹 페이지 기본 설정
st.set_page_config(page_title="윤정님의 키워드 마스터", layout="wide")

st.title("🎯 네이버 플레이스 키워드 자동 생성기 (편집 모드)")
st.info("윤정님의 상권/메뉴 데이터를 실시간으로 수정하여 키워드를 생성할 수 있습니다.")

# 2. 상권 기본 데이터베이스
DB = {
   "연희시오 야탑점": [
        "성남시",
        "야탑",
        "정자동",
        "분당구",
        "경기도 성남시",
        "야탑1동",
        "경기도 성남시 분당구 정자동",
        "야탑2동",
        "경기도 성남시 분당구",
        "야탑동",
        "경기도 성남시 분당구 이매동",
        "경기도 성남시 분당구 서현동",
        "경기도 성남시 분당구 수내동",
        "야탑역",
        "이매역",
        "서현역",
        "수내역",
        "판교역",
        "모란역",
        "태평역",
        "수진역"
    ],

# 3. 사이드바: 상권 및 메뉴 편집 섹션
with st.sidebar:
    st.header("⚙️ 실시간 데이터 편집")
    
    # --- 상권 편집 ---
    st.subheader("📍 1. 상권 설정")
    selected_area = st.selectbox("수정할 상권 선택", list(DB.keys()) + ["직접 입력"])
    
    if selected_area == "직접 입력":
        area_name = st.text_input("새 상권 이름", value="신규지역")
        default_locs = "랜드마크1, 랜드마크2"
    else:
        area_name = selected_area
        default_locs = ", ".join(DB[selected_area])
    
    edited_locs_raw = st.text_area("랜드마크 편집 (쉼표로 구분)", value=default_locs, help="단어 사이에 쉼표(,)를 넣어주세요.")
    final_locs = [x.strip() for x in edited_locs_raw.split(",") if x.strip()]

    st.write("---")

    # --- 메뉴 및 마케팅 편집 ---
    st.subheader("🍱 2. 메뉴 및 테마 설정")
    
    # 기본값 설정
    default_themes = "가성비, 청첩장모임, 분위기좋은, 회식하기좋은, 내돈내산, 찐맛집, 부모님식사, 데이트코스, 조용한, 룸있는"
    default_menus = "솥밥, 스테이크솥밥, 장어솥밥, 한정식, 점심, 저녁, 히츠마부시, 룸식당, 반상, 한상"
    default_suffixes = "맛집, 추천, 식당, 추천맛집, 추천식당, 점심맛집, 저녁맛집"

    edited_themes_raw = st.text_area("마케팅 테마 편집", value=default_themes)
    edited_menus_raw = st.text_area("메뉴/업종 편집", value=default_menus)
    edited_suffixes_raw = st.text_area("접미사 편집", value=default_suffixes)

    themes = [x.strip() for x in edited_themes_raw.split(",") if x.strip()]
    menus = [x.strip() for x in edited_menus_raw.split(",") if x.strip()]
    suffixes = [x.strip() for x in edited_suffixes_raw.split(",") if x.strip()]

# 4. 메인 화면: 선택 확인 및 생성
st.subheader(f"🔍 현재 설정: {area_name}")
col1, col2, col3 = st.columns(3)
col1.write("**현재 랜드마크:**")
col1.caption(", ".join(final_locs))
col2.write("**현재 테마:**")
col2.caption(", ".join(themes[:5]) + "...")
col3.write("**현재 메뉴:**")
col3.caption(", ".join(menus[:5]) + "...")

st.write("---")

# 5. 키워드 생성 로직
if st.button("🚀 키워드 조합 생성 및 결과 보기"):
    # 모든 경우의 수 조합 (Cartesian Product)
    combos = list(itertools.product(final_locs, themes, menus, suffixes))
    
    results = []
    for c in combos:
        kw = f"{c[0]} {c[1]} {c[2]} {c[3]}"
        if len(kw) <= 25: # 네이버 광고 가이드 준수
            results.append(kw)
    
    # 중복 제거
    results = list(set(results))
    
    if results:
        df = pd.DataFrame(results, columns=["네이버 플레이스 광고 키워드"])
        
        st.success(f"✅ 총 {len(df):,}개의 유효 키워드가 생성되었습니다!")
        
        # 결과 테이블 및 다운로드
        st.dataframe(df, use_container_width=True)
        
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="💾 생성된 키워드 엑셀(CSV) 파일로 받기",
            data=csv,
            file_name=f"naver_keywords_{area_name}.csv",
            mime="text/csv",
        )
    else:
        st.warning("조합된 키워드가 없습니다. 설정을 확인해 주세요.")
