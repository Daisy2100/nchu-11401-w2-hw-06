-- SQLite 資料庫初始化腳本
-- 用於創建天氣資料表

-- 刪除舊表（如果存在）
DROP TABLE IF EXISTS weather;

-- 創建天氣資料表
CREATE TABLE weather (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location TEXT NOT NULL,                -- 地區名稱
    min_temp REAL,                         -- 最低溫度（攝氏）
    max_temp REAL,                         -- 最高溫度（攝氏）
    weather_desc TEXT,                     -- 天氣描述
    pop TEXT,                              -- 降雨機率
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP  -- 資料時間戳記
);

-- 創建索引以提高查詢效能
CREATE INDEX idx_location ON weather(location);
CREATE INDEX idx_timestamp ON weather(timestamp);

-- 顯示資料表結構
.schema weather
