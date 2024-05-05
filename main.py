import os
import requests


url = 'https://tululu.org/txt.php'

response = requests.get(url)
response.raise_for_status()

if not os.path.exists('books'):
  os.makedirs('books')

for id in range(1, 11):
  payload = {'id': id}
  response = requests.get(url, params=payload)
  response.raise_for_status()

  book = f'books/id{id}.txt'

  with open(book, 'wb') as file:
    file.write(response.content)
