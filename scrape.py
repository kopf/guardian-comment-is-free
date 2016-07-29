#!/usr/bin/env python
from datetime import datetime
import json

from bs4 import BeautifulSoup
import requests


URL = 'https://www.theguardian.com/uk/commentisfree/rss'
DATASET_FILE = '/home/kopf/dev/guardian/dataset.json'


def main():
    run_start = datetime.utcnow().strftime('%Y-%m-%d.%H_%M_%S')
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "html.parser")
    with open(DATASET_FILE, 'r') as f:
        dataset = json.load(f)
    altered = False
    for item in soup.find_all('item'):
        if item.guid.text not in dataset:
            altered = True
            author = getattr(item, 'dc:creator')
            if author:
                author = author.text
            date = getattr(item, 'dc:date')
            if date:
                date = date.text
            dataset[item.guid.text] = {
                'title': item.title.text,
                'description': item.description.text,
                'author': author,
                'date': date
            }
    if altered:
        with open(DATASET_FILE, 'w') as f:
            f.write(json.dumps(dataset, indent=4))
            

if __name__ == '__main__':
    main()
