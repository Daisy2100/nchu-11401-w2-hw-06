import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

def get_movies_data():
    """
    爬取開眼電影網的本週新片排行榜
    """
    url = "http://www.atmovies.com.tw/movie/next/0/"
    
    try:
        # 設定 headers 模擬瀏覽器
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # 發送 GET 請求
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        response.raise_for_status()
        
        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        movies = []
        
        # 找到電影列表
        movie_list = soup.find_all('li', class_='filmListItem')
        
        for idx, movie in enumerate(movie_list, 1):
            try:
                movie_data = {}
                
                # 排名
                movie_data['rank'] = idx
                
                # 電影標題
                title_tag = movie.find('a', class_='filmTitle')
                if title_tag:
                    movie_data['title'] = title_tag.text.strip()
                else:
                    movie_data['title'] = 'N/A'
                
                # 英文標題
                en_title_tag = movie.find('div', class_='filmTitle')
                if en_title_tag:
                    en_title = en_title_tag.find('a', class_='filmTitle')
                    if en_title and en_title.get('title'):
                        movie_data['en_title'] = en_title.get('title')
                    else:
                        movie_data['en_title'] = 'N/A'
                else:
                    movie_data['en_title'] = 'N/A'
                
                # 上映日期
                date_tag = movie.find('span', class_='date')
                if date_tag:
                    movie_data['release_date'] = date_tag.text.strip()
                else:
                    movie_data['release_date'] = 'N/A'
                
                # 評分
                rating_tag = movie.find('span', class_='starScore')
                if rating_tag:
                    rating_text = rating_tag.text.strip()
                    try:
                        movie_data['rating'] = float(rating_text)
                    except ValueError:
                        movie_data['rating'] = 0.0
                else:
                    movie_data['rating'] = 0.0
                
                # 片長
                runtime_tag = movie.find('span', string=lambda text: text and '片長' in text)
                if runtime_tag:
                    movie_data['runtime'] = runtime_tag.text.strip()
                else:
                    movie_data['runtime'] = 'N/A'
                
                movies.append(movie_data)
                
                # 避免請求過快
                time.sleep(0.1)
                
            except Exception as e:
                print(f"解析電影 {idx} 時發生錯誤: {e}")
                continue
        
        return movies
        
    except requests.RequestException as e:
        print(f"請求錯誤: {e}")
        return None
    except Exception as e:
        print(f"解析錯誤: {e}")
        return None

def save_to_csv(movies, filename='movies_data.csv'):
    """
    將電影資料儲存為 CSV 檔案
    """
    try:
        df = pd.DataFrame(movies)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"資料已儲存至 {filename}")
        return df
    except Exception as e:
        print(f"儲存檔案錯誤: {e}")
        return None

def display_movies(df):
    """
    顯示電影資料
    """
    if df is not None and not df.empty:
        print("\n本週新片排行榜:")
        print("=" * 80)
        for _, row in df.iterrows():
            print(f"\n排名: {row['rank']}")
            print(f"片名: {row['title']}")
            if row['en_title'] != 'N/A':
                print(f"英文片名: {row['en_title']}")
            print(f"上映日期: {row['release_date']}")
            print(f"評分: {row['rating']}")
            if row['runtime'] != 'N/A':
                print(f"{row['runtime']}")
            print("-" * 80)

def main():
    print("正在爬取電影資料...")
    print("資料來源: 開眼電影網")
    
    movies = get_movies_data()
    
    if movies:
        print(f"\n成功爬取 {len(movies)} 部電影資料")
        
        # 儲存資料
        df = save_to_csv(movies)
        
        # 顯示資料
        display_movies(df)
        
        # 統計資訊
        if df is not None and not df.empty:
            print("\n統計資訊:")
            print(f"電影總數: {len(df)}")
            if 'rating' in df.columns:
                avg_rating = df['rating'].mean()
                print(f"平均評分: {avg_rating:.2f}")
                top_movie = df.loc[df['rating'].idxmax()]
                print(f"最高評分: {top_movie['title']} ({top_movie['rating']})")
    else:
        print("無法獲取電影資料")

if __name__ == "__main__":
    main()
