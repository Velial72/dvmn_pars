# Парсер книг с сайта tululu.org

Программа поможет скачать книги с сайта [tululu.org](https://tululu.org/) в формате .txt. Она также сохранит обложку, название, автора, жанры и комментарии пользователей. Можно скачать несколько книг сразу, указав нужный диапазон.

## Предварительная настройка
1. Для запуска у вас должны быть установлены Python 3 и pip.

2. Скачай код.

3. Создай виртуальную среду, используя [virtualenv/venv](https://docs.python.org/3/library/venv.html).

4. Установи все пакеты используемые программой. Используй `requirements.txt`:
   ```
   pip install -r requirements.txt
   ```

## Как запустить загрузку книг

Запусти код указав нужный диапазон, Например с 20 по 30:
   ```
   python3 main.py -s 20 -e 30
   ```

## Как запустить скачивание книг пачками по страницам с жанром фантастика

1. Для запуска используй команду:
   ```
   python3 parse_tululu_category.py
   ```
2. Можно указать дополнительные параметры:
 * `-sp` указать с какой страницы качать
 * `-ep` указать до какой страницы качать
 * `-f` указать название директории для скачивания
 * `-i` не скачивать картинки
 * `-t` не скачивать текст

Например команда ниже скачает описание книг, автора, жанр и отзывы, но не скачает текст книги и е е обложку. Будут задействованы страницы с 27 по 55 и создана папка "тест" куда загрузятся все скачанные файлы:
   ```
   python3 parse_tululu_category.py -sp 27 -ep 55 -i -t -f test
   ```

## Сайт с домашней библиотекой:

Пример рабочего сайта можно посмотреть [тут](https://velial72.github.io/dvmn_pars/pages/index1.html)

## Сайт с домашней библиотекой (офлайн):

1. Необходимо выполнить команду:
   ```
   python3 render_website.py
   ```
2. Сайт будет доступен по [ссылке](http://127.0.0.1:5500/pages/index1.html)

## Вариант запуска для ленивых:

1. Открыть директорию `Pages`
2. Кликнуть на файл `index1.html`

## Цель проекта

Код написан в образовательных целях.