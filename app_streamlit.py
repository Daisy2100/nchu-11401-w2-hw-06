import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# 設定頁面配置
st.set_page_config(
    page_title="天氣與電影資訊系統",
    page_icon="🌤️",
    layout="wide"
)

def load_weather_data():
    """載入天氣資料"""
    try:
        if os.path.exists('weather_data.json'):
            with open('weather_data.json', 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"載入天氣資料錯誤: {e}")
    return None

def load_movies_data():
    """載入電影資料"""
    try:
        if os.path.exists('movies_data.csv'):
            return pd.read_csv('movies_data.csv')
    except Exception as e:
        st.error(f"載入電影資料錯誤: {e}")
    return None

def display_weather():
    """顯示天氣資訊"""
    st.header("🌤️ 天氣資訊")
    
    weather_data = load_weather_data()
    
    if weather_data:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("城市", weather_data.get('city', 'N/A'))
        
        with col2:
            st.metric("溫度", weather_data.get('temperature', 'N/A'))
        
        with col3:
            st.metric("天氣", weather_data.get('weather', 'N/A'))
        
        with col4:
            st.metric("濕度", weather_data.get('humidity', 'N/A'))
        
        st.info(f"資料更新時間: {weather_data.get('timestamp', 'N/A')}")
    else:
        st.warning("尚未有天氣資料,請先執行 part1_weather.py")

def display_movies():
    """顯示電影資訊"""
    st.header("🎬 本週新片排行榜")
    
    movies_df = load_movies_data()
    
    if movies_df is not None and not movies_df.empty:
        # 顯示統計資訊
        st.subheader("📊 統計資訊")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("電影總數", len(movies_df))
        
        with col2:
            avg_rating = movies_df['rating'].mean() if 'rating' in movies_df.columns else 0
            st.metric("平均評分", f"{avg_rating:.1f}")
        
        with col3:
            if 'rating' in movies_df.columns:
                top_movie = movies_df.loc[movies_df['rating'].idxmax(), 'title']
                st.metric("最高評分電影", top_movie)
        
        # 顯示電影列表
        st.subheader("📋 電影列表")
        
        # 搜尋功能
        search_term = st.text_input("搜尋電影", "")
        
        if search_term:
            filtered_df = movies_df[movies_df['title'].str.contains(search_term, case=False, na=False)]
        else:
            filtered_df = movies_df
        
        # 排序選項
        sort_by = st.selectbox("排序方式", ["排名", "評分", "片名"])
        
        if sort_by == "排名":
            filtered_df = filtered_df.sort_values('rank')
        elif sort_by == "評分":
            if 'rating' in filtered_df.columns:
                filtered_df = filtered_df.sort_values('rating', ascending=False)
        elif sort_by == "片名":
            filtered_df = filtered_df.sort_values('title')
        
        # 顯示資料表
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )
        
        # 圖表顯示
        if 'rating' in movies_df.columns:
            st.subheader("📈 評分分布")
            st.bar_chart(movies_df.set_index('title')['rating'])
    else:
        st.warning("尚未有電影資料,請先執行 movies_crawler.py")

def main():
    """主程式"""
    st.title("🌤️ 天氣與電影資訊系統")
    st.markdown("---")
    
    # 側邊欄
    with st.sidebar:
        st.header("選單")
        page = st.radio("選擇頁面", ["天氣資訊", "電影資訊", "全部顯示"])
        
        st.markdown("---")
        st.info("""
        ### 使用說明
        1. 執行 `part1_weather.py` 取得天氣資料
        2. 執行 `movies_crawler.py` 取得電影資料
        3. 使用此應用程式查看資料
        """)
    
    # 根據選擇顯示內容
    if page == "天氣資訊":
        display_weather()
    elif page == "電影資訊":
        display_movies()
    else:
        display_weather()
        st.markdown("---")
        display_movies()
    
    # 頁尾
    st.markdown("---")
    st.caption(f"最後更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
