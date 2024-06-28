from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from pathlib import Path


json_path = Path('books/Book_info.json')
with open(json_path, 'r', encoding='utf8') as file:
    books_data = json.load(file)

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('index.html')

books_info = [
    {
        'title': book.get('title'),
        'author': book.get('author'),
        'image': book.get('img_file_path')
    }
    for book in books_data
]
print(books_info)
rendered_page = template.render(books=books_info)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()