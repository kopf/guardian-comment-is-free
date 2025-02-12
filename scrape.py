#!/usr/bin/env -S uv run --script
# /// script
# dependencies = [
#     "beautifulsoup4==4.9.3",
#     "requests==2.25.0",
# ]
# ///

from datetime import datetime
import json
import sys

from bs4 import BeautifulSoup
import requests


URL = 'https://www.theguardian.com/uk/commentisfree/rss'
DATASET_FILE = sys.argv[-1]
REPLACEMENTS = {
    "Steve Bell\u2019s If ...": "",
    "Steve Bell's If \u2026": "",
}


def main():
    run_start = datetime.utcnow().strftime('%Y-%m-%d.%H_%M_%S')
    with open(DATASET_FILE, 'r') as f:
        dataset = json.load(f)
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "html.parser")
    altered = False
    for item in soup.find_all('item'):
        if '/commentisfree/' in item.guid.text and item.guid.text not in dataset:
            altered = True
            author = getattr(item, 'dc:creator')
            if author:
                author = author.text
            date = getattr(item, 'dc:date')
            if date:
                date = date.text
            title = item.title.text
            for find, replace in REPLACEMENTS.items():
                title = title.replace(find, replace)
            dataset[item.guid.text] = {
                'title': title,
                'description': item.description.text,
                'author': author,
                'date': date
            }
    print("Dataset contains {} items".format(len(dataset)))
    if altered:
        print("Saving...")
        with open(DATASET_FILE, 'w') as f:
            f.write(json.dumps(dataset, indent=4))
            

if __name__ == '__main__':
    main()
