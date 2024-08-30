import json
import os
from dotenv import load_dotenv
from models import Author, Quote

# Завантаження змінних середовища з .env файлу
load_dotenv()

def load_authors(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        authors_data = json.load(file)
        for author_data in authors_data:
            Author(**author_data).save()

def load_quotes(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)
        for quote_data in quotes_data:
            author = Author.objects(fullname=quote_data['author']).first()
            if author:
                Quote(
                    tags=quote_data['tags'],
                    author=author,
                    quote=quote_data['quote']
                ).save()

if __name__ == '__main__':
    load_authors('authors.json')
    load_quotes('qoutes.json')  # Виправлено назву файлу
