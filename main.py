import requests
from requests.exceptions import HTTPError
import argparse

from help_functions import download_txt, check_for_redirect


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

    for id in range(args.start_id, args.end_id+1):
        payload = {'id': id}
        download_url = f'{main_page}txt.php'
        response = requests.get(download_url, params=payload)
        response.raise_for_status()

        try:    
            check_for_redirect(response)
        except HTTPError as http_err:
            print(http_err)
            continue
        
        download_txt(url=main_page, response=response, id=id)


if __name__ == '__main__':
    main()