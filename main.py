import os
import requests
from requests.exceptions import HTTPError


url = 'https://tululu.org/txt.php'

if not os.path.exists('books'):
  os.makedirs('books')


def check_for_redirect(response):
  if response.url == 'https://tululu.org/':
    raise HTTPError(f'error')


for id in range(1, 11):
  payload = {'id': id}

  book = f'books/id{id}.txt'
  response = requests.get(url, params=payload)
  response.raise_for_status()
  
  try:
    check_for_redirect(response)
  except HTTPError as http_err:
    print(http_err)
    continue

  with open(book, 'wb') as file:
      file.write(response.content)