import glob
import json
import math
import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server


BOOKS_PER_PAGE = 10

def load_books_data(json_path):
    with open(json_path, 'r', encoding='utf8') as file:
        return json.load(file)


def prepare_books_info(books_data):
    return [
        {
            'title': book.get('title'),
            'author': book.get('author'),
            'genres': book.get('genres'),
            'image': book.get('img_file_path'),
            'link': book.get('txt_file_path'),
        }
        for book in books_data
    ]


def update(books_info, template, total_pages):
    for page_num in range(1, total_pages + 1):
        start_index = (page_num - 1) * BOOKS_PER_PAGE
        end_index = start_index + BOOKS_PER_PAGE
        current_page_books = books_info[start_index:end_index]

        rendered_page = template.render(books=current_page_books, page_num=page_num, total_pages=total_pages)

        with open(f'pages/index{page_num}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


def rebuild(env, json_path):
    books_data = load_books_data(json_path)
    books_info = prepare_books_info(books_data)
    total_pages = math.ceil(len(books_info) / BOOKS_PER_PAGE)
    template = env.get_template('template.html')
    update(books_info, template, total_pages)


def main():
    json_files = glob.glob('*/Book_info.json')
    if not json_files:
        raise FileNotFoundError("Не удалось найти файл Book_info.json в подкаталогах.")
    json_path = Path(json_files[0])

    os.makedirs('pages', exist_ok=True)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    rebuild(env, json_path)

    server = Server()
    server.watch('template.html', lambda: rebuild(env, json_path))
    server.watch(str(json_path), lambda: rebuild(env, json_path))

    server.serve(root='.')


if __name__ == "__main__":
    main()