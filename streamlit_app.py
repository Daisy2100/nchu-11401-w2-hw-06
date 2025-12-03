"""
Streamlit 應用程式 - 顯示 CWA 天氣資料
從 SQLite 資料庫讀取並視覺化天氣資訊
"""

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# 頁面設定
st.set_page_config(
    page_title="CWA 天氣資料視覺化",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自訂 CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)
def load_weather_data():
    """從 SQLite 資料庫載入天氣資料"""
    try:
        conn = sqlite3.connect('data.db')
        query = "SELECT * FROM weather ORDER BY location"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"載入資料時發生錯誤: {e}")
        return pd.DataFrame()

def display_statistics(df):
    """顯示統計資訊"""
    st.subheader("📊 統計資訊")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "總地區數",
            len(df),
            help="資料庫中的地區總數"
        )
    
    with col2:
        avg_min = df['min_temp'].mean()
        st.metric(
            "平均最低溫",
            f"{avg_min:.1f}°C" if not pd.isna(avg_min) else "N/A",
            help="所有地區的平均最低溫度"
        )
    
    with col3:
        avg_max = df['max_temp'].mean()
        st.metric(
            "平均最高溫",
            f"{avg_max:.1f}°C" if not pd.isna(avg_max) else "N/A",
            help="所有地區的平均最高溫度"
        )
    
    with col4:
        if not df.empty and 'timestamp' in df.columns:
            update_time = df['timestamp'].iloc[0]
            st.metric(
                "資料更新時間",
                update_time.split()[1] if ' ' in str(update_time) else update_time,
                help="最後更新時間"
            )

def display_weather_table(df):
    """顯示天氣資料表格"""
    st.subheader("🗂️ 天氣資料表")
    
    # 搜尋功能
    search = st.text_input("🔍 搜尋地區", placeholder="輸入地區名稱...")
    
    if search:
        df_display = df[df['location'].str.contains(search, case=False, na=False)]
    else:
        df_display = df
    
    # 排序選項
    col1, col2 = st.columns([1, 3])
    with col1:
        sort_by = st.selectbox(
            "排序方式",
            ["地區", "最低溫", "最高溫"],
            help="選擇排序依據"
        )
    
    if sort_by == "地區":
        df_display = df_display.sort_values('location')
    elif sort_by == "最低溫":
        df_display = df_display.sort_values('min_temp')
    elif sort_by == "最高溫":
        df_display = df_display.sort_values('max_temp', ascending=False)
    
    # 顯示資料表
    st.dataframe(
        df_display[['location', 'min_temp', 'max_temp', 'weather_desc', 'pop']],
        column_config={
            "location": st.column_config.TextColumn("地區", width="medium"),
            "min_temp": st.column_config.NumberColumn("最低溫 (°C)", format="%.1f"),
            "max_temp": st.column_config.NumberColumn("最高溫 (°C)", format="%.1f"),
            "weather_desc": st.column_config.TextColumn("天氣描述", width="medium"),
            "pop": st.column_config.TextColumn("降雨機率", width="small"),
        },
        use_container_width=True,
        hide_index=True
    )
    
    st.info(f"顯示 {len(df_display)} 筆資料")

def display_temperature_chart(df):
    """顯示溫度圖表"""
    st.subheader("📈 溫度分布圖")
    
    tab1, tab2, tab3 = st.tabs(["長條圖", "散點圖", "箱型圖"])
    
    with tab1:
        # 溫度範圍長條圖
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='最低溫',
            x=df['location'],
            y=df['min_temp'],
            marker_color='lightblue'
        ))
        
        fig.add_trace(go.Bar(
            name='最高溫',
            x=df['location'],
            y=df['max_temp'],
            marker_color='coral'
        ))
        
        fig.update_layout(
            title="各地區溫度比較",
            xaxis_title="地區",
            yaxis_title="溫度 (°C)",
            barmode='group',
            height=500,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # 最低溫 vs 最高溫散點圖
        fig = px.scatter(
            df,
            x='min_temp',
            y='max_temp',
            text='location',
            title='最低溫 vs 最高溫',
            labels={'min_temp': '最低溫 (°C)', 'max_temp': '最高溫 (°C)'},
            color='max_temp',
            size='max_temp',
            color_continuous_scale='RdYlBu_r',
            height=500
        )
        
        fig.update_traces(textposition='top center')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # 箱型圖
        fig = go.Figure()
        
        fig.add_trace(go.Box(
            y=df['min_temp'],
            name='最低溫',
            marker_color='lightblue'
        ))
        
        fig.add_trace(go.Box(
            y=df['max_temp'],
            name='最高溫',
            marker_color='coral'
        ))
        
        fig.update_layout(
            title="溫度分布箱型圖",
            yaxis_title="溫度 (°C)",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)

def get_region_coordinates():
    """取得台灣各地區的經緯度座標"""
    coordinates = {
        '北部地區': {'lat': 25.0330, 'lon': 121.5654},
        '中部地區': {'lat': 24.1477, 'lon': 120.6736},
        '南部地區': {'lat': 22.6273, 'lon': 120.3014},
        '東北部地區': {'lat': 24.7021, 'lon': 121.7378},
        '東部地區': {'lat': 23.9871, 'lon': 121.6015},
        '東南部地區': {'lat': 22.7583, 'lon': 121.1444}
    }
    return coordinates

def display_interactive_map(df):
    """顯示互動式溫度分布圖"""
    st.subheader("🗺️ 互動式溫度分布圖")
    
    # 控制面板
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    
    with col1:
        time_option = st.radio(
            "時間選擇",
            ["今日", "平均值"],
            horizontal=True,
            help="選擇要顯示的時間範圍"
        )
    
    with col2:
        temp_type = st.radio(
            "溫度類型",
            ["最高溫", "最低溫", "平均溫"],
            horizontal=True
        )
    
    with col3:
        show_values = st.checkbox("顯示數據", value=True)
    
    with col4:
        auto_refresh = st.checkbox("自動更新", value=False)
    
    # 根據選擇顯示不同溫度
    if temp_type == "最高溫":
        temp_col = 'max_temp'
        title = "最高溫度分布圖"
        color_scale = "Reds"
    elif temp_type == "最低溫":
        temp_col = 'min_temp'
        title = "最低溫度分布圖"
        color_scale = "Blues"
    else:
        df['avg_temp'] = (df['max_temp'] + df['min_temp']) / 2
        temp_col = 'avg_temp'
        title = "平均溫度分布圖"
        color_scale = "RdYlBu_r"
    
    # 添加座標資訊
    coordinates = get_region_coordinates()
    df['lat'] = df['location'].map(lambda x: coordinates.get(x, {}).get('lat', 23.5))
    df['lon'] = df['location'].map(lambda x: coordinates.get(x, {}).get('lon', 121.0))
    
    # 創建左右兩欄布局
    col_left, col_right = st.columns([1, 2])
    
    with col_left:
        # 左側：溫度列表
        st.markdown(f"### 📋 {title}")
        st.markdown(f"**更新時間**: {datetime.now().strftime('%Y/%m/%d %H:%M')}")
        st.markdown("---")
        
        for idx, row in df.iterrows():
            temp_value = row[temp_col]
            
            # 根據溫度決定顏色
            if temp_value >= 28:
                color = "🔴"
            elif temp_value >= 24:
                color = "🟠"
            elif temp_value >= 20:
                color = "🟡"
            elif temp_value >= 16:
                color = "🟢"
            else:
                color = "🔵"
            
            st.markdown(f"{color} **{row['location']}**: `{temp_value:.1f}°C`")
            st.caption(f"天氣: {row['weather_desc']}")
    
    with col_right:
        # 右側：台灣地圖
        fig = go.Figure()
        
        # 添加散點圖（地區標記）
        fig.add_trace(go.Scattergeo(
            lon=df['lon'],
            lat=df['lat'],
            text=df['location'] + '<br>' + df[temp_col].round(1).astype(str) + '°C',
            mode='markers+text',
            marker=dict(
                size=df[temp_col] * 2,
                color=df[temp_col],
                colorscale=color_scale,
                showscale=True,
                colorbar=dict(
                    title="溫度 (°C)",
                    x=1.02
                ),
                line=dict(width=1, color='white')
            ),
            textposition="top center",
            textfont=dict(size=12, color='black', family='Arial Black'),
            hovertemplate='<b>%{text}</b><extra></extra>'
        ))
        
        # 設定地圖樣式 - 類似中央氣象局的配色
        fig.update_geos(
            center=dict(lon=120.9, lat=23.7),
            projection_scale=35,
            visible=True,
            resolution=50,
            showcountries=True,
            countrycolor="darkgray",
            showcoastlines=True,
            coastlinecolor="darkgray",
            showland=True,
            landcolor="white",  # 改為白色陸地
            showocean=True,
            oceancolor="#E8F4F8",  # 淺藍色海洋
            projection_type="mercator",
            bgcolor="white"  # 背景改為白色
        )
        
        fig.update_layout(
            title=dict(
                text=f"台灣 {title}<br><sub>{datetime.now().strftime('%Y/%m/%d %H:%M')}</sub>",
                x=0.5,
                xanchor='center'
            ),
            height=600,
            margin=dict(l=0, r=0, t=50, b=0),
            geo=dict(
                lonaxis=dict(range=[119.5, 122.5]),
                lataxis=dict(range=[21.5, 25.5])
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # 如果啟用自動更新
    if auto_refresh:
        st.info("⏱️ 資料將每30秒自動更新一次")
        time.sleep(30)
        st.rerun()

def display_top_locations(df):
    """顯示溫度排行"""
    st.subheader("🏆 溫度排行榜")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**最高溫 TOP 5**")
        top_hot = df.nlargest(5, 'max_temp')[['location', 'max_temp', 'weather_desc']]
        for idx, row in top_hot.iterrows():
            st.write(f"🔥 {row['location']}: **{row['max_temp']:.1f}°C** - {row['weather_desc']}")
    
    with col2:
        st.write("**最低溫 TOP 5**")
        top_cold = df.nsmallest(5, 'min_temp')[['location', 'min_temp', 'weather_desc']]
        for idx, row in top_cold.iterrows():
            st.write(f"❄️ {row['location']}: **{row['min_temp']:.1f}°C** - {row['weather_desc']}")

def main():
    """主程式"""
    # 標題
    st.markdown('<p class="main-header">🌤️ 中央氣象局天氣資料視覺化系統</p>', unsafe_allow_html=True)
    
    # 側邊欄
    with st.sidebar:
        st.image("https://www.cwa.gov.tw/Data/fcst_img/SFCcombo.jpg", caption="中央氣象局")
        st.markdown("---")
        st.info("""
        ### 📋 資料來源
        - **來源**: 中央氣象局 OpenData API
        - **資料集**: F-A0010-001
        - **資料庫**: SQLite (data.db)
        
        ### 🔄 更新資料
        執行以下命令更新資料:
        ```bash
        python part1_cwa_weather.py
        ```
        """)
        
        if st.button("🔄 重新載入資料", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    # 載入資料
    df = load_weather_data()
    
    if df.empty:
        st.error("⚠️ 無法載入資料,請確認:")
        st.error("1. 已執行 part1_cwa_weather.py")
        st.error("2. data.db 檔案存在")
        st.error("3. 資料庫中有資料")
        return
    
    # 顯示內容
    # 最上方：互動式溫度分布圖
    display_interactive_map(df)
    st.markdown("---")
    
    display_statistics(df)
    st.markdown("---")
    
    display_weather_table(df)
    st.markdown("---")
    
    display_temperature_chart(df)
    st.markdown("---")
    
    display_top_locations(df)
    
    # 頁尾
    st.markdown("---")
    st.caption(f"© 2025 CWA Weather Dashboard | 最後更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
