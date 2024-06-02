import os
import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename, sanitize_filepath


def check_for_redirect(response):
    if response.url == 'https://tululu.org/':
        raise HTTPError(f'error')


def get_name(book_id = id):
    url = f'http://tululu.org/b{book_id}/'
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('h1')
    clear_title = title_tag.text.split('::')
    # book_author =  clear_title[1].strip()
    book_name = clear_title[0].strip()
    return book_name


def download_txt(folder='books/'):
    if not os.path.exists(folder):
        os.makedirs(folder)

    for id in range(1, 11):
        filename = get_name(id)
        book_name = sanitize_filename(filename=filename)
        book_path = sanitize_filepath(os.path.join(folder, f'{id}.{book_name}.txt'))

        payload = {'id': id}
        url = 'https://tululu.org/txt.php'
        response = requests.get(url, params=payload)
        response.raise_for_status()
        
        try:
            check_for_redirect(response)
        except HTTPError as http_err:
            print(http_err)
            continue

        with open(book_path, 'wb') as file:
            file.write(response.content)


if __name__ == '__main__':
    download_txt()