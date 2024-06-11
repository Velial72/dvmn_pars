import os
import requests
import json
from bs4 import BeautifulSoup
from time import sleep
from urllib.parse import urljoin
from help_functions import parse_book_page, download_txt, download_image, check_for_redirect
from requests.exceptions import HTTPError


def main():
    all_books_info = []
    main_page = f'https://tululu.org/'

    if os.path.exists('Book_info.json'):
        with open('Book_info.json', 'r', encoding='utf8') as json_file:
            try:
                all_books_info = json.load(json_file)
            except json.JSONDecodeError:
                all_books_info = []

    for page in range(1, 2):
        
        response = requests.get(url=f'{main_page}l55/{page}/')
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'lxml')
        book_selector = '.d_book'
        book_tags = soup.select(selector=book_selector)

        for book_tag in book_tags:
            book_url_tag = book_tag.select_one(selector=('a'))['href']
            book_url = urljoin(main_page, book_url_tag)
            conn = True
            while conn:
                try:   
                    
                    response = requests.get(book_url, allow_redirects=False)
                    response.raise_for_status()

                    check_for_redirect(response)
                    
                    book_response_content = response.content
                    parsed_book_page = parse_book_page(book_html=book_response_content, url=book_url)
                    book_title = parsed_book_page.get('title')
                    download_txt(url=parsed_book_page.get('txt_url'),
                                    filename=f'{book_title}')
                    download_image(url=parsed_book_page.get('image_url'))

                    parsed_book_page.pop('txt_url', None)
                    parsed_book_page.pop('image_url', None)
                    all_books_info.append(parsed_book_page
                                          )
                    with open('Book_info', 'w', encoding='utf8') as json_file:
                        json.dump(all_books_info, json_file, ensure_ascii=False, indent=4)
                    conn = False
                except HTTPError as http_err:
                    print(http_err)
                    conn = False
                except requests.exceptions.ConnectionError as conn_err:
                    print(conn_err)
                    sleep(180)


if __name__ == '__main__':
    main()