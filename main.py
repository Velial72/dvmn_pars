import argparse
from time import sleep

import requests
from requests.exceptions import HTTPError

from help_functions import (
    parse_book_page, 
    download_txt, 
    download_image, 
    check_for_redirect
)


def main():
    main_page = 'https://tululu.org/'
    
    parser = argparse.ArgumentParser(description='Тут можно задать с какой по какую книгу скачать')
    parser.add_argument('-s', '--start_id', 
                        help='с какого номера качать', 
                        type=int, 
                        default=1)
    parser.add_argument('-e', '--end_id', 
                        help='с какого до какого номера качать', 
                        type=int, 
                        default=10)
    args = parser.parse_args()

    for book_id in range(args.start_id, args.end_id+1):
        book_url = f'{main_page }b{book_id}/'
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
                                filename=f'{book_id} {book_title}')
                download_image(url=parsed_book_page.get('image_url'))
                conn = False
            except HTTPError as http_err:
                print(http_err)
                conn = False
            except requests.exceptions.ConnectionError as conn_err:
                print(conn_err)
                sleep(180)
            
           


if __name__ == '__main__':
    main()
