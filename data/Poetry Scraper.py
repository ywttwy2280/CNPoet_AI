import requests
from bs4 import BeautifulSoup
import json
import time

# 定义请求头，模拟浏览器访问
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# 爬取的页数范围
MAX_PAGES = 30
BASE_URL = "https://www.en84.com/poetry"

# 诗歌数据列表
poems = []

def get_poetry_links(page_url):
    """获取诗歌详情页的链接"""
    response = requests.get(page_url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to fetch {page_url}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    links = []
    for article in soup.find_all("article"):
        link_tag = article.find("a")
        if link_tag and link_tag["href"]:
            links.append(link_tag["href"])
    return links

def get_poetry_content(poetry_url):
    """获取诗歌内容"""
    response = requests.get(poetry_url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to fetch {poetry_url}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("h1", class_="entry-title").get_text(strip=True)
    
    # 诗歌正文
    content_div = soup.find("div", class_="entry-content")
    if not content_div:
        return None

    paragraphs = content_div.find_all("p")
    if not paragraphs or len(paragraphs) < 2:
        return None
    
    # 假设正文前半部分是中文，后半部分是英文
    middle_idx = len(paragraphs) // 2
    chinese_text = "\n".join([p.get_text(strip=True) for p in paragraphs[:middle_idx]])
    english_text = "\n".join([p.get_text(strip=True) for p in paragraphs[middle_idx:]])

    return {
        "title": title,
        "chinese": chinese_text,
        "english": english_text,
        "url": poetry_url
    }

# 遍历所有页面
for page in range(1, MAX_PAGES + 1):
    page_url = BASE_URL if page == 1 else f"{BASE_URL}/page/{page}/"
    print(f"Fetching: {page_url}")
    
    poetry_links = get_poetry_links(page_url)
    for poetry_url in poetry_links:
        print(f"Scraping: {poetry_url}")
        poetry_data = get_poetry_content(poetry_url)
        if poetry_data:
            poems.append(poetry_data)
        
        time.sleep(1)  # 避免触发反爬虫

# 保存为 JSON 文件
with open("poems.json", "w", encoding="utf-8") as f:
    json.dump(poems, f, ensure_ascii=False, indent=4)

print(f"爬取完成，共保存 {len(poems)} 首诗歌到 poems.json")
