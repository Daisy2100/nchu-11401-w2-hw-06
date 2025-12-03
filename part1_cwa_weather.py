"""
Part 1: 中央氣象局 (CWA) 天氣資料爬蟲
使用 CWA OpenData API 下載 F-A0010-001 資料集
解析 JSON 並存入 SQLite 資料庫
"""

import requests
import sqlite3
import json
from datetime import datetime

# CWA API 設定
API_KEY = "CWA-1FFDDAEC-161F-46A3-BE71-93C32C52829F"
API_URL = f"https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-A0010-001?Authorization={API_KEY}&downloadType=WEB&format=JSON"

def download_cwa_data():
    """下載 CWA JSON 資料"""
    print("正在下載 CWA 天氣資料...")
    try:
        response = requests.get(API_URL, timeout=30)
        response.raise_for_status()
        data = response.json()
        print("✓ 資料下載成功!")
        return data
    except requests.RequestException as e:
        print(f"✗ 下載失敗: {e}")
        return None

def parse_weather_data(data):
    """解析 JSON 資料,提取各地區溫度資訊"""
    weather_records = []
    
    try:
        # 取得資料集
        dataset = data.get('cwaopendata', {}).get('dataset', {})
        locations = dataset.get('locations', [{}])[0].get('location', [])
        
        print(f"\n正在解析 {len(locations)} 個地區的天氣資料...")
        
        for location in locations:
            location_name = location.get('locationName', 'N/A')
            
            # 取得天氣元素
            weather_elements = location.get('weatherElement', [])
            
            # 初始化資料記錄
            record = {
                'location': location_name,
                'min_temp': None,
                'max_temp': None,
                'weather_desc': None,
                'pop': None,  # 降雨機率
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # 解析各種天氣元素
            for element in weather_elements:
                element_name = element.get('elementName', '')
                time_data = element.get('time', [])
                
                if time_data:
                    first_time = time_data[0]
                    parameter = first_time.get('parameter', {})
                    
                    if element_name == 'MinT':  # 最低溫度
                        record['min_temp'] = parameter.get('parameterName', 'N/A')
                    elif element_name == 'MaxT':  # 最高溫度
                        record['max_temp'] = parameter.get('parameterName', 'N/A')
                    elif element_name == 'Wx':  # 天氣現象
                        record['weather_desc'] = parameter.get('parameterName', 'N/A')
                    elif element_name == 'PoP':  # 降雨機率
                        record['pop'] = parameter.get('parameterName', 'N/A')
            
            weather_records.append(record)
            print(f"  ✓ {location_name}: 最低溫 {record['min_temp']}°C, 最高溫 {record['max_temp']}°C")
        
        print(f"\n✓ 成功解析 {len(weather_records)} 筆天氣資料")
        return weather_records
        
    except Exception as e:
        print(f"✗ 解析資料時發生錯誤: {e}")
        return []

def init_database():
    """初始化 SQLite 資料庫"""
    print("\n正在初始化資料庫...")
    
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    # 建立 weather 資料表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT NOT NULL,
            min_temp REAL,
            max_temp REAL,
            weather_desc TEXT,
            pop TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    print("✓ 資料庫初始化完成!")
    return conn

def save_to_database(weather_records, conn):
    """將天氣資料存入 SQLite"""
    print("\n正在儲存資料到資料庫...")
    
    cursor = conn.cursor()
    
    # 清空舊資料
    cursor.execute('DELETE FROM weather')
    
    # 插入新資料
    for record in weather_records:
        try:
            # 轉換溫度為浮點數
            min_temp = float(record['min_temp']) if record['min_temp'] and record['min_temp'] != 'N/A' else None
            max_temp = float(record['max_temp']) if record['max_temp'] and record['max_temp'] != 'N/A' else None
            
            cursor.execute('''
                INSERT INTO weather (location, min_temp, max_temp, weather_desc, pop, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                record['location'],
                min_temp,
                max_temp,
                record['weather_desc'],
                record['pop'],
                record['timestamp']
            ))
        except Exception as e:
            print(f"  ✗ 插入 {record['location']} 時發生錯誤: {e}")
    
    conn.commit()
    print(f"✓ 成功儲存 {len(weather_records)} 筆資料到資料庫!")

def display_sample_data(conn):
    """顯示資料庫中的範例資料"""
    print("\n資料庫內容預覽（前 5 筆）:")
    print("=" * 100)
    
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM weather LIMIT 5')
    rows = cursor.fetchall()
    
    for row in rows:
        print(f"ID: {row[0]}, 地區: {row[1]}, 最低溫: {row[2]}°C, 最高溫: {row[3]}°C, 天氣: {row[4]}, 降雨率: {row[5]}%")
    
    print("=" * 100)

def main():
    """主程式"""
    print("=" * 100)
    print("中央氣象局 (CWA) 天氣資料爬蟲")
    print("=" * 100)
    
    # 1. 下載資料
    data = download_cwa_data()
    if not data:
        print("程式結束")
        return
    
    # 2. 解析資料
    weather_records = parse_weather_data(data)
    if not weather_records:
        print("程式結束")
        return
    
    # 3. 初始化資料庫
    conn = init_database()
    
    # 4. 儲存資料
    save_to_database(weather_records, conn)
    
    # 5. 顯示範例資料
    display_sample_data(conn)
    
    # 關閉資料庫連線
    conn.close()
    
    print("\n✓ 所有作業完成!")
    print(f"✓ 資料庫檔案: data.db")
    print(f"✓ 請執行 'streamlit run streamlit_app.py' 查看資料視覺化")

if __name__ == "__main__":
    main()
