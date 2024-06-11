import os
import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
from pathvalidate import sanitize_filename, sanitize_filepath
from urllib.parse import urljoin


def check_for_redirect(response: requests.models.Response, file):
    '''Checks for redirects and, if so, raises an HTTPError'''
    if response.is_redirect:
        raise HTTPError(f'Data for {file} not found.')


def download_txt(url, filename, folder='books/'):
    os.makedirs(folder, exist_ok=True)
        
    book_name = sanitize_filename(filename=filename)
    book_path = sanitize_filepath(os.path.join(folder, f'{id}.{book_name}.txt'))
    book_response = requests.get(url)
    check_for_redirect(book_response,  file=filename)
    book_response.raise_for_status()
    with open(book_path, 'wb') as file:
        file.write(book_response.content)
    print('Книга скачана')


def download_image(url, folder='images/'):
    os.makedirs('images/', exist_ok=True)

    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    filename = url.split('/')

    img_name = sanitize_filename(filename=filename[-1])
    img_path = sanitize_filepath(os.path.join(folder, img_name))
    
    with open(img_path, 'wb') as file:
        file.write(response.content)



def parse_book_page(book_html: bytes, url):
    soup = BeautifulSoup(book_html, 'lxml')
    title_and_author = soup.find(id='content').find('h1').text.split('::')
    title, author = (el.strip() for el in title_and_author)

    genres_tag = soup.find('span', class_='d_book').find_all('a')
    book_genres = [genre.text for genre in genres_tag]

    comments_tag = soup.find(id='content').find_all(class_='black')
    comments = [commit.text for commit in comments_tag]

    book_txt_tag = soup.find(id='content').find(
                    'a', title=f'{title} - скачать книгу txt')
    if book_txt_tag:
        raise HTTPError('Книга не найдена')
    txt_relative_link = book_txt_tag["href"]
    txt_url = urljoin(url, txt_relative_link)

    img_tag = soup.find(class_='bookimage').find('img').get('src')
    book_image = urljoin(url, img_tag)

    return {
        'title': title,
        'author': author,
        'genres': book_genres,
        'comments': comments,
        'txt_url': txt_url,
        'image_url': book_image,
    }