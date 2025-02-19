import requests
from bs4 import BeautifulSoup
import json
import os

def get_poetry_links(base_url):
    response = requests.get(base_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    poetry_links = []
    for link in soup.select('.entry-title a'):
        poetry_links.append(link['href'])
    
    return poetry_links

def get_poetry_content(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    title = soup.find('h1', class_='entry-title').text.strip()
    content = soup.find('div', class_='entry-content')
    
    paragraphs = content.find_all('p')
    chinese, english = [], []
    
    for p in paragraphs:
        text = p.text.strip()
        if text:
            if any(ord(char) > 127 for char in text):  # 如果包含中文字符
                chinese.append(text)
            else:
                english.append(text)
    
    return {
        'title': title,
        'chinese': chinese,
        'english': english,
        'url': url
    }

def save_to_json(data, filename='poetry.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    base_url = 'https://www.en84.com/poetry/'
    poetry_links = get_poetry_links(base_url)
    
    poetry_list = []
    for link in poetry_links:
        try:
            poetry = get_poetry_content(link)
            poetry_list.append(poetry)
            print(f"Fetched: {poetry['title']}")
        except Exception as e:
            print(f"Failed to fetch {link}: {e}")
    
    save_to_json(poetry_list)
    print("Poetry data saved to poetry.json")

if __name__ == '__main__':
    main()
