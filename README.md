# nchu-11401-w2-hw-06 — Lecture 13 課堂練習

此專案包含兩部分作業：
1. **Part 1**: 中央氣象局資料爬蟲 + SQLite + Streamlit
2. **Part 2**: 電影網站爬蟲 + CSV 輸出

## 🗂️ 專案結構

```
.
├── Dockerfile              # SQLite Docker 容器
├── docker-compose.yml      # Docker Compose 設定
├── requirements.txt        # Python 依賴套件
├── part1_weather.py        # Part 1: 天氣資料爬蟲
├── app_streamlit.py        # Streamlit 應用
├── movies_crawler.py       # Part 2: 電影爬蟲
├── data/                   # 資料目錄（掛載到 Docker）
│   └── data.db            # SQLite 資料庫（執行後產生）
└── movie.csv              # 電影資料 CSV（執行後產生）
```

## 🚀 快速開始

### 1. 建立資料夾
```bash
mkdir -p data
```

### 2. 啟動 Docker 容器
```bash
docker-compose up -d --build
```

這會建立一個包含 SQLite3 的容器，並將本機 `./data` 掛載到容器內。

### 3. 安裝 Python 依賴
建議使用虛擬環境：
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 4. 執行 Part 1：天氣資料爬蟲
```bash
python part1_weather.py
```

這會：
- 從中央氣象局下載 JSON 資料
- 解析各地區的天氣資訊
- 將資料存入 `./data/data.db` 的 `weather` 表

### 5. 啟動 Streamlit 應用
```bash
streamlit run app_streamlit.py
```

開啟瀏覽器訪問 `http://localhost:8501`，你會看到天氣資料表格。

**📸 記得截圖此頁面作為作業證明！**

### 6. 執行 Part 2：電影爬蟲
```bash
python movies_crawler.py
```

這會爬取 `https://ssr1.scrape.center/` 的 1-10 頁，並產生 `movie.csv`。

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