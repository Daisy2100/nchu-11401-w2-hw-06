import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def get_weather_data():
    """
    爬取中央氣象署的天氣資料
    """
    url = "https://www.cwa.gov.tw/V8/C/W/County/County.html?CID=63"
    
    try:
        # 發送 GET 請求
        response = requests.get(url)
        response.raise_for_status()
        
        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 找到天氣資訊區塊
        weather_data = {}
        
        # 獲取縣市名稱
        city_name = soup.find('h2', class_='CtyName')
        if city_name:
            weather_data['city'] = city_name.text.strip()
        
        # 獲取當前溫度
        temp = soup.find('span', class_='tem-C is-active')
        if temp:
            weather_data['temperature'] = temp.text.strip()
        
        # 獲取天氣描述
        weather_desc = soup.find('span', class_='wea')
        if weather_desc:
            weather_data['weather'] = weather_desc.text.strip()
        
        # 獲取濕度
        humidity = soup.find('span', string='相對濕度')
        if humidity:
            humidity_value = humidity.find_next('span', class_='num')
            if humidity_value:
                weather_data['humidity'] = humidity_value.text.strip() + '%'
        
        # 獲取時間
        weather_data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return weather_data
        
    except requests.RequestException as e:
        print(f"請求錯誤: {e}")
        return None
    except Exception as e:
        print(f"解析錯誤: {e}")
        return None

def save_to_json(data, filename='weather_data.json'):
    """
    將天氣資料儲存為 JSON 檔案
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"資料已儲存至 {filename}")
    except Exception as e:
        print(f"儲存檔案錯誤: {e}")

def main():
    print("正在爬取天氣資料...")
    weather_data = get_weather_data()
    
    if weather_data:
        print("\n天氣資訊:")
        print(json.dumps(weather_data, ensure_ascii=False, indent=2))
        
        # 儲存資料
        save_to_json(weather_data)
    else:
        print("無法獲取天氣資料")

if __name__ == "__main__":
    main()
