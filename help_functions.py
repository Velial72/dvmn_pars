import os
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
from pathvalidate import sanitize_filename, sanitize_filepath


def check_for_redirect(response: requests.models.Response):
    '''Checks for redirects and, if so, raises an HTTPError'''
    if response.is_redirect:
        raise HTTPError(f'Data not found.')


def download_txt(url, filename, folder):
    os.makedirs(folder, exist_ok=True)
        
    book_name = sanitize_filename(filename=filename)
    book_path = sanitize_filepath(os.path.join(folder, f'{id}.{book_name}.txt'))
    book_response = requests.get(url)
    check_for_redirect(book_response)
    book_response.raise_for_status()
    with open(book_path, 'wb') as file:
        file.write(book_response.content)
    print('Книга скачана')


def download_image(url, folder):
    os.makedirs(folder, exist_ok=True)

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

    genres_select = '.d_book a'
    genres_tag = soup.select(selector=genres_select)
    book_genres = [genre.text for genre in genres_tag]

    comments_select = ('#content .black')
    comments_tag = soup.select(selector=comments_select)
    comments = [commit.text for commit in comments_tag]

    txt_select = f'#content a[title="{title} - скачать книгу txt"]'
    book_txt_tag = soup.select_one(txt_select)
    if not book_txt_tag:
        raise HTTPError('Книга не найдена')
    txt_relative_link = book_txt_tag["href"]
    txt_url = urljoin(url, txt_relative_link)

    img_select = '.bookimage img'
    img_tag = soup.select_one(selector=img_select)
    img_src = img_tag['src']
    book_image = urljoin(url, img_src)

    return {
        'title': title,
        'author': author,
        'genres': book_genres,
        'comments': comments,
        'txt_url': txt_url,
        'image_url': book_image,
    }


def get_last_page_number(url):
    response = requests.get(url=f'{url}l55/')
    response.raise_for_status()
    check_for_redirect(response)
    soup = BeautifulSoup(response.content, 'lxml')
    page_select = '.npage'
    pages = soup.select(selector=page_select)
    last_page_tag = pages[-1]
    last_page_number = last_page_tag.text
    return int(last_page_number)