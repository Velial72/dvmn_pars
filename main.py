import os
import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename, sanitize_filepath
from urllib.parse import urljoin, urlparse


def check_for_redirect(response):
    if response.url == 'https://tululu.org/':
        raise HTTPError(f'error')


def parse_book_page(book_id = id):
    url = f'http://tululu.org/b{book_id}/'
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('h1')
    clear_title = title_tag.text.split('::')
    
    book_author =  clear_title[1].strip()
    book_name = clear_title[0].strip()

    print(book_name)
    print()
    print(book_author)
    print()

    genres_tag = soup.find('span', class_='d_book').find_all('a')
    book_genre = [genre.text for genre in genres_tag]
    print(book_genre)

    comments_tag = soup.find(id='content').find_all(class_='black')
    comments = [commit.text for commit in comments_tag]

    # for i in comments:
    #     print(i)
    print()
    print()

    img_tag = soup.find('div', class_='bookimage').find('img')['src']
    book_image = urljoin('https://tululu.org/', img_tag)
    download_image(url=book_image)

    return book_name


def download_txt(folder='books/'):
    if not os.path.exists(folder):
        os.makedirs(folder)

    if not os.path.exists('images/'):
        os.makedirs('images/')

    for id in range(1, 11):
        payload = {'id': id}
        url = 'https://tululu.org/txt.php'
        response = requests.get(url, params=payload)
        response.raise_for_status()
        
        try:
            check_for_redirect(response)
        except HTTPError as http_err:
            print(http_err)
            continue
        
        filename = parse_book_page(id)
        book_name = sanitize_filename(filename=filename)
        book_path = sanitize_filepath(os.path.join(folder, f'{id}.{book_name}.txt'))

        with open(book_path, 'wb') as file:
            file.write(response.content)


def download_image(url, folder='images/'):
    response = requests.get(url)
    response.raise_for_status()
    filename = response.url.split('/')

    img_name = sanitize_filename(filename=filename[-1])
    img_path = sanitize_filepath(os.path.join(folder, img_name))
    with open(img_path, 'wb') as file:
        file.write(response.content)


if __name__ == '__main__':
    download_txt()