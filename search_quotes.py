import os
import redis
import json
from mongoengine import connect
from models import Quote, Author

# Підключення до бази даних MongoDB та Redis
connect(
    db='authors_db',
    host=os.getenv('MONGO_URI'),
    username=os.getenv('DB_ADMIN'),
    password=os.getenv('DB_PASSWORD')
)

cache = redis.StrictRedis.from_url(os.getenv('REDIS_URL'), decode_responses=True)

def search_quotes_by_tag(tag):
    cached_result = cache.get(f'tag:{tag}')
    if cached_result:
        return json.loads(cached_result)
    
    quotes = Quote.objects(tags__in=[tag])
    result = [quote.to_mongo().to_dict() for quote in quotes]
    
    cache.set(f'tag:{tag}', json.dumps(result))
    return result

def search_quotes_by_tags(tags):
    tag_list = tags.split(',')
    result = []
    for tag in tag_list:
        cached_result = cache.get(f'tag:{tag}')
        if cached_result:
            result.extend(json.loads(cached_result))
        else:
            quotes = Quote.objects(tags__in=[tag])
            tag_result = [quote.to_mongo().to_dict() for quote in quotes]
            cache.set(f'tag:{tag}', json.dumps(tag_result))
            result.extend(tag_result)
    return result

def search_quotes_by_author(name):
    author = Author.objects(fullname__icontains=name).first()
    if not author:
        return []
    quotes = Quote.objects(author=author)
    return [quote.to_mongo().to_dict() for quote in quotes]

def search_quotes(name=None, tag=None, tags=None):
    if name:
        return search_quotes_by_author(name)
    if tag:
        return search_quotes_by_tag(tag)
    if tags:
        return search_quotes_by_tags(tags)
    return []

if __name__ == '__main__':
    while True:
        command = input("Enter command (name: <author>, tag: <tag>, tags: <tags>, exit): ")
        if command.startswith("name:"):
            name = command[len("name:"):].strip()
            results = search_quotes(name=name)
        elif command.startswith("tag:"):
            tag = command[len("tag:"):].strip()
            results = search_quotes(tag=tag)
        elif command.startswith("tags:"):
            tags = command[len("tags:"):].strip()
            results = search_quotes(tags=tags)
        elif command == "exit":
            break
        else:
            print("Invalid command.")
            continue
        
        for result in results:
            print(json.dumps(result, ensure_ascii=False, indent=2))
