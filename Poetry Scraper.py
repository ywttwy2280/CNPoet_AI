import requests
from bs4 import BeautifulSoup
import json
import os

def fetch_poetry_links(base_url, pages=30):
    links = []
    for page in range(2, pages):
        url = f"{base_url}/page/{page}/"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for article in soup.find_all('h2', class_='entry-title'):
            link = article.find('a')
            if link and link['href']:
                links.append(link['href'])
    return links

def fetch_poem_content(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    title = soup.find('h1', class_='entry-title').get_text(strip=True) if soup.find('h1', class_='entry-title') else "Untitled"
    content_div = soup.find('div', class_='entry-content')
    
    if not content_div:
        return None
    
    paragraphs = content_div.find_all('p')
    chinese_lines, english_lines = [], []
    
    for p in paragraphs:
        text = p.get_text(strip=True)
        if any(c.isalpha() for c in text):
            english_lines.append(text)
        else:
            chinese_lines.append(text)
    
    return {
        'title': title,
        'chinese': '\n'.join(chinese_lines),
        'english': '\n'.join(english_lines)
    }

def save_to_json(data, filename='poems.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    base_url = "https://www.en84.com/poetry"
    poem_links = fetch_poetry_links(base_url, pages=30)
    
    poems = []
    for link in poem_links:
        poem = fetch_poem_content(link)
        if poem:
            poems.append(poem)
    
    save_to_json(poems)
    print(f"Saved {len(poems)} poems to poems.json")

if __name__ == "__main__":
    main()
