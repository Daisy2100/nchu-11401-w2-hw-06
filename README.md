# NCHU 11401 Week 2 Homework 06 - Lecture 13 課堂練習

## 📚 課堂練習：資料爬蟲 + SQLite + Streamlit

這個專案包含兩個主要部分：
1. **Part 1**: 中央氣象局 (CWA) 天氣資料爬蟲與視覺化
2. **Part 2**: SSR 電影網站爬蟲

---

## 🗂️ 專案結構

```
nchu-11401-w2-hw-06/
├── part1_cwa_weather.py      # Part 1: CWA 天氣爬蟲
├── streamlit_app.py           # Part 1: Streamlit 視覺化應用
├── init_db.sql                # SQLite 資料庫初始化腳本
├── part2_movie_crawler.py     # Part 2: 電影爬蟲
├── requirements.txt           # Python 依賴套件
├── Dockerfile                 # Docker 映像檔
├── docker-compose.yml         # Docker Compose 設定
├── .gitignore                 # Git 忽略檔案
├── data.db                    # SQLite 資料庫（執行後產生）
└── movie.csv                  # 電影資料 CSV（執行後產生）
```

## 🚀 快速開始

### 方法一：本地執行（推薦）

#### 1. 安裝 Python 依賴
```bash
pip install -r requirements.txt
```

#### 2. 執行 Part 1：天氣資料爬蟲
```bash
python part1_cwa_weather.py
```

這會：
- 使用 CWA OpenData API 下載 F-A0010-001 資料集
- 解析各地區的天氣資訊（最低溫、最高溫、天氣描述、降雨機率）
- 將資料存入 `data.db` 的 `weather` 表

#### 3. 啟動 Streamlit 應用
```bash
streamlit run streamlit_app.py
```

開啟瀏覽器訪問 `http://localhost:8501`，你會看到：
- 📊 統計資訊儀表板
- 🗂️ 可搜尋與排序的天氣資料表
- 📈 溫度分布圖表（長條圖、散點圖、箱型圖）
- 🏆 溫度排行榜

**📸 記得截圖此頁面作為作業證明！**

#### 4. 執行 Part 2：電影爬蟲
```bash
python part2_movie_crawler.py
```

這會爬取 `https://ssr1.scrape.center/` 的 1-10 頁，並產生 `movie.csv`。

---

### 方法二：使用 Docker

#### 1. 先執行爬蟲取得資料（在本地）
```bash
pip install -r requirements.txt
python part1_cwa_weather.py
python part2_movie_crawler.py
```

#### 2. 啟動 Docker 容器
```bash
docker-compose up -d --build
```

#### 3. 在瀏覽器開啟
```
http://localhost:8501
```

#### 4. 查看日誌
```bash
docker-compose logs -f
```

#### 5. 停止服務
```bash
docker-compose down
```

## 📊 資料庫結構

### weather 表
```sql
CREATE TABLE weather (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_name TEXT NOT NULL,
    element_name TEXT,
    description TEXT,
    start_time TEXT,
    end_time TEXT,
    value TEXT
);
```

## 🔧 使用的技術

- **Python 3.x**
- **requests** - HTTP 請求
- **beautifulsoup4** - HTML 解析
- **sqlite3** - 資料庫操作（Python 內建）
- **streamlit** - Web 介面
- **pandas** - 資料處理
- **Docker** - SQLite 容器化

## 📝 API 資訊

- **中央氣象局 API Key**: `CWA-1FFDDAEC-161F-46A3-BE71-93C32C52829F`
- **Dataset**: F-A0010-001
- **網站**: https://opendata.cwa.gov.tw/

## 🐛 常見問題

### Docker 容器無法啟動
```bash
# 檢查容器狀態
docker ps -a

# 重新啟動
docker-compose down
docker-compose up -d --build
```

### 找不到 data.db
確保你已經執行過 `part1_weather.py`，資料庫檔案會自動建立在 `./data/data.db`。

### Streamlit 無法連接資料庫
確保 `./data/data.db` 存在且有資料。

## 📦 交付內容

### Part 1
- ✅ `part1_weather.py` - 天氣爬蟲原始碼
- ✅ `./data/data.db` - SQLite 資料庫
- ✅ `app_streamlit.py` - Streamlit 應用原始碼
- ✅ Streamlit 截圖（需自行截圖）

### Part 2
- ✅ `movies_crawler.py` - 電影爬蟲原始碼
- ✅ `movie.csv` - 電影資料 CSV

## 👨‍💻 作者

- **學號/姓名**: Daisy2100
- **課程**: NCHU 114-01 Lecture 13
- **日期**: 2025-12-03

## 📄 授權

此專案僅供教育用途。