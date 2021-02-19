import requests
from bs4 import BeautifulSoup
import csv

CSV = 'films.csv'
HOST = 'https://www.kinopoisk.ru/'
URL = 'https://www.kinopoisk.ru/lists/top250/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
}

def get_html(url, page_params=''):
    r = requests.get(url, headers = HEADERS, params = page_params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='desktop-rating-selection-film-item')
    films = []

    for item in items:
        films.append(
            {
                'title':item.find('p', class_='selection-film-item-meta__name').get_text(),
                'rating': item.find('span', class_='rating__value rating__value_positive').get_text(),
                'additional': item.find('span', class_='selection-film-item-meta__meta-additional-item').get_text(),
                'link': HOST + item.find('a', class_='selection-film-item-meta__link').get('href')
            }
        )
    return films

def parser():
    pages = int(input('Количество страниц для парсинга: ').strip())
    html = get_html(URL)
    if html.status_code == 200:
        films = []
        for page in range(1, pages + 1):
            print('Обработка страницы:', page)
            html = get_html(URL, page_params={'page': page})
            films.extend(get_content(html.text))
            writeToCvs(films, CSV)
        print('Завершено')
    else:
        print('Ошибка')

def writeToCvs(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название фильма', 'Рейтинг', 'Страна производства', 'Ссылка на фильм'])
        for item in items:
            writer.writerow([item['title'], item['rating'], item['additional'], item['link']])

parser()