
import urllib.request
import xml.etree.ElementTree as ET
import json
import re
import html
from html.parser import HTMLParser

FEED_URL = "https://www.technologyreview.com/feed/"

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []

    def handle_data(self, data):
        self.text.append(data)

def clean_text(value):
    parser = TextExtractor()
    parser.feed(html.unescape(value or ""))
    return re.sub(r"\s+", " ", " ".join(parser.text)).strip()

def get_text(element, name):
    item = element.find(name)
    return item.text if item is not None and item.text else ""

response = urllib.request.urlopen(FEED_URL, timeout=30)
root = ET.fromstring(response.read())

articles = []

for item in root.findall(".//item"):
    title = clean_text(get_text(item, "title"))
    link = get_text(item, "link").strip()
    date = get_text(item, "pubDate").strip()
    description = clean_text(get_text(item, "description"))

    if title and link and date:
        articles.append({
            "title": title,
            "link": link,
            "date": date,
            "description": description
        })

articles.sort(
    key=lambda article: article["date"],
    reverse=True
)

articles = articles[:10]

with open("news.json", "w", encoding="utf-8") as file:
    json.dump(articles, file, indent=2, ensure_ascii=False)

print(f"Updated news.json with {len(articles)} articles.")
