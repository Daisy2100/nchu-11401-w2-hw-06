import requests
import json

API_URL = "https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-A0010-001?Authorization=CWA-1FFDDAEC-161F-46A3-BE71-93C32C52829F&downloadType=WEB&format=JSON"

print("正在下載資料...")
response = requests.get(API_URL, timeout=30)
data = response.json()

print("\n=== 資料結構分析 ===")
print(f"最上層 keys: {list(data.keys())}")

# 保存完整資料以供檢查
with open('cwa_data_full.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n完整資料已儲存至 cwa_data_full.json")
print("\n前 3000 字元預覽:")
print(json.dumps(data, ensure_ascii=False, indent=2)[:3000])
