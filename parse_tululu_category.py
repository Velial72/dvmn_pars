import argparse
import json
import os
from pathlib import Path
from time import sleep
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError

from help_functions import (
    parse_book_page, 
    download_txt, 
    download_image, 
    check_for_redirect, 
    get_last_page_number
)


def main():
    base_dir = Path(__file__).resolve().parent
    path_to_dir = base_dir
    books_descriptions = []
    main_page = 'https://tululu.org/'

    parser = argparse.ArgumentParser(description='Тут можно задать с какой по какую страницы скачать')
    parser.add_argument('-sp', '--start_page', 
                        help='с какой страницы качать', 
                        type=int, 
                        default=1)
    parser.add_argument('-ep', '--end_page', 
                        help='с какого до какой страницы качать', 
                        type=int, 
                        default=get_last_page_number(url=main_page))
    parser.add_argument('-f', '--dest_folder', 
                        help='указать название директории для загрузок', 
                        type=str)
    parser.add_argument('-i', '--skip_imgs', 
                        help='не скачивать картинки', 
                        action='store_true')
    parser.add_argument('-t', '--skip_txt', 
                        help='не скачивать книги', 
                        action='store_true')
    
    args = parser.parse_args()
    start_page = args.start_page
    end_page = args.end_page

    if args.dest_folder:
        os.makedirs(args.dest_folder, exist_ok=True)
        path_to_dir = base_dir.joinpath(args.dest_folder)

    if os.path.exists('Book_info.json'):
        with open('Book_info.json', 'r', encoding='utf8') as json_file:
            try:
                books_descriptions = json.load(json_file)
            except json.JSONDecodeError:
                books_descriptions = []

    for page in range(start_page, end_page+1 ):
        flag = True
        while flag:
            try:
                response = requests.get(url=f'{main_page}l55/{page}/')
                response.raise_for_status()
                check_for_redirect(response)
                flag = False
            except HTTPError as http_err:
                        print(http_err)
            except requests.exceptions.ConnectionError as conn_err:
                    print(conn_err)
                    sleep(180)
        soup = BeautifulSoup(response.content, 'lxml')
        book_selector = '.d_book'
        book_tags = soup.select(selector=book_selector)

        for book_tag in book_tags:
            book_url_tag = book_tag.select_one(selector=('a'))['href']
            image_url=f'{main_page}l55/{page}/'
            book_url = urljoin(image_url, book_url_tag)
            conn = True
            while conn:
                try:   
                    
                    response = requests.get(book_url, allow_redirects=False)
                    response.raise_for_status()

                    check_for_redirect(response)
                    
                    book_response_content = response.content
                    parsed_book_page = parse_book_page(book_html=book_response_content, url=book_url)
                    book_title = parsed_book_page.get('title')
                    if not args.skip_txt:
                        download_txt(url=parsed_book_page.get('txt_url'),
                                        filename=f'{book_title}', folder=f'{path_to_dir}/books/')
                    if not args.skip_imgs:    
                        download_image(url=parsed_book_page.get('image_url'), folder=f'{path_to_dir}/images/')

                    parsed_book_page.pop('txt_url', None)
                    parsed_book_page.pop('image_url', None)
                    books_descriptions.append(parsed_book_page)
                    
                    conn = False
                except HTTPError as http_err:
                    print(http_err)
                    conn = False
                except requests.exceptions.ConnectionError as conn_err:
                    print(conn_err)
                    sleep(180)
    file_path = path_to_dir / 'Book_info.json'
    with open(file_path, 'w', encoding='utf8') as json_file:
        json.dump(books_descriptions, json_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()