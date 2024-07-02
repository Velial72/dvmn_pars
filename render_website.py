import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
import glob
from pathlib import Path
import math
from livereload import Server


json_files = glob.glob('*/Book_info.json')
if not json_files:
    raise FileNotFoundError("Не удалось найти файл Book_info.json в подкаталогах.")
json_path = Path(json_files[0])

with open(json_path, 'r', encoding='utf8') as file:
    books_data = json.load(file)

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

books_info = [
    {
        'title': book.get('title'),
        'author': book.get('author'),
        'genres': book.get('genres'),
        'image': book.get('img_file_path'),
        'link': book.get('txt_file_path'),
    }
    for book in books_data
]


books_per_page = 10
total_pages = math.ceil(len(books_info) / books_per_page)

os.makedirs('pages', exist_ok=True)

for page_num in range(1, total_pages + 1):
    start_index = (page_num - 1) * books_per_page
    end_index = start_index + books_per_page
    current_page_books = books_info[start_index:end_index]

    rendered_page = template.render(books=current_page_books, page_num=page_num, total_pages=total_pages)

    with open(f'pages/index{page_num}.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def update():
    for page_num in range(1, total_pages + 1):
        start_index = (page_num - 1) * books_per_page
        end_index = start_index + books_per_page
        current_page_books = books_info[start_index:end_index]

        rendered_page = template.render(books=current_page_books, page_num=page_num, total_pages=total_pages)

        with open(f'pages/index{page_num}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


server = Server()

server.watch('template.html', update)
server.watch('books/Book_info.json', update)

server.serve(root='')