"""
Part 2: SSR 電影網站爬蟲
爬取 https://ssr1.scrape.center/ 的 10 頁電影資料
解析電影名稱、圖片 URL、評分、類型等資訊並存成 CSV
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime

BASE_URL = "https://ssr1.scrape.center"

def get_page_html(page_num):
    """獲取指定頁面的 HTML"""
    url = f"{BASE_URL}/page/{page_num}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        print(f"正在爬取第 {page_num} 頁: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"✗ 爬取第 {page_num} 頁失敗: {e}")
        return None

def parse_movie_data(html):
    """解析 HTML 中的電影資訊"""
    movies = []
    
    try:
        soup = BeautifulSoup(html, 'html.parser')
        
        # 找到所有電影卡片
        movie_items = soup.find_all('div', class_='el-card')
        
        for item in movie_items:
            try:
                movie = {}
                
                # 電影名稱
                name_tag = item.find('a', class_='name')
                if name_tag:
                    movie['name'] = name_tag.text.strip()
                    movie['url'] = BASE_URL + name_tag.get('href', '')
                else:
                    movie['name'] = 'N/A'
                    movie['url'] = 'N/A'
                
                # 電影圖片 URL
                img_tag = item.find('img', class_='cover')
                if img_tag:
                    movie['image_url'] = img_tag.get('src', 'N/A')
                else:
                    movie['image_url'] = 'N/A'
                
                # 評分
                score_tag = item.find('p', class_='score')
                if score_tag:
                    try:
                        movie['rating'] = float(score_tag.text.strip())
                    except ValueError:
                        movie['rating'] = 0.0
                else:
                    movie['rating'] = 0.0
                
                # 類型
                categories_div = item.find('div', class_='categories')
                if categories_div:
                    category_buttons = categories_div.find_all('button')
                    categories = [btn.text.strip() for btn in category_buttons]
                    movie['categories'] = ', '.join(categories) if categories else 'N/A'
                else:
                    movie['categories'] = 'N/A'
                
                # 上映地區
                region_tag = item.find('div', class_='info')
                if region_tag:
                    region_spans = region_tag.find_all('span')
                    if len(region_spans) >= 1:
                        movie['region'] = region_spans[0].text.strip()
                    else:
                        movie['region'] = 'N/A'
                    
                    # 上映時間
                    if len(region_spans) >= 3:
                        movie['release_date'] = region_spans[2].text.strip()
                    else:
                        movie['release_date'] = 'N/A'
                else:
                    movie['region'] = 'N/A'
                    movie['release_date'] = 'N/A'
                
                movies.append(movie)
                print(f"  ✓ 解析電影: {movie['name']} (評分: {movie['rating']})")
                
            except Exception as e:
                print(f"  ✗ 解析單部電影時發生錯誤: {e}")
                continue
        
        return movies
        
    except Exception as e:
        print(f"✗ 解析 HTML 時發生錯誤: {e}")
        return []

def crawl_all_pages(total_pages=10):
    """爬取所有頁面的電影資料"""
    all_movies = []
    
    print("=" * 100)
    print("開始爬取 SSR 電影網站")
    print("=" * 100)
    
    for page in range(1, total_pages + 1):
        # 獲取 HTML
        html = get_page_html(page)
        
        if html:
            # 解析電影資料
            movies = parse_movie_data(html)
            all_movies.extend(movies)
            print(f"✓ 第 {page} 頁完成,共獲取 {len(movies)} 部電影\n")
        else:
            print(f"✗ 第 {page} 頁失敗\n")
        
        # 避免請求過快,加入延遲
        if page < total_pages:
            time.sleep(1)
    
    return all_movies

def save_to_csv(movies, filename='movie.csv'):
    """將電影資料存成 CSV"""
    try:
        df = pd.DataFrame(movies)
        
        # 添加爬取時間戳記
        df['crawl_timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 重新排序欄位
        column_order = ['name', 'rating', 'categories', 'region', 'release_date', 'image_url', 'url', 'crawl_timestamp']
        df = df[column_order]
        
        # 儲存為 CSV
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print("=" * 100)
        print(f"✓ 資料已儲存至 {filename}")
        print(f"✓ 總共爬取 {len(movies)} 部電影")
        print("=" * 100)
        
        return df
        
    except Exception as e:
        print(f"✗ 儲存 CSV 時發生錯誤: {e}")
        return None

def display_statistics(df):
    """顯示統計資訊"""
    if df is None or df.empty:
        return
    
    print("\n統計資訊:")
    print("-" * 100)
    print(f"電影總數: {len(df)}")
    print(f"平均評分: {df['rating'].mean():.2f}")
    print(f"最高評分: {df['rating'].max():.2f}")
    print(f"最低評分: {df['rating'].min():.2f}")
    
    print("\n評分最高的 5 部電影:")
    top_movies = df.nlargest(5, 'rating')[['name', 'rating', 'categories']]
    for idx, row in top_movies.iterrows():
        print(f"  🎬 {row['name']}: {row['rating']} 分 - {row['categories']}")
    
    print("\n電影類型分布:")
    all_categories = []
    for cats in df['categories']:
        if cats != 'N/A':
            all_categories.extend([c.strip() for c in cats.split(',')])
    
    if all_categories:
        from collections import Counter
        category_counts = Counter(all_categories)
        for cat, count in category_counts.most_common(10):
            print(f"  {cat}: {count} 部")
    
    print("-" * 100)

def main():
    """主程式"""
    # 爬取所有頁面
    movies = crawl_all_pages(total_pages=10)
    
    if not movies:
        print("✗ 未爬取到任何電影資料")
        return
    
    # 儲存為 CSV
    df = save_to_csv(movies, 'movie.csv')
    
    # 顯示統計資訊
    display_statistics(df)
    
    print("\n✓ 所有作業完成!")
    print("✓ 電影資料已儲存至 movie.csv")

if __name__ == "__main__":
    main()
