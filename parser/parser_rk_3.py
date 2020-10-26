import requests
from bs4 import BeautifulSoup as BS
from openpyxl import Workbook
import os, shutil
import threading


start_page = input('Начальная страница каталога -> ')
HOST = 'https://www.rusklimat.ru'
urls = []
item_url = []
resp = []
article = []
price = []
name = []
status = []
span_status = None

#расчет количества страниц
def pages_count(html):
    r = requests.get(html, params=None)
    page_bs = BS(r.content, 'lxml')
    pagination = page_bs.select('div.paginator > ul > li > a')
    if pagination:
        return int(pagination[-1].string)
    else:
        return 1


#запрос всех страниц в каталоге
def get_urls():
    print('Начало парсинга')
    for x in range(1, pages_count(start_page)+1):
        urls.append(requests.get(start_page + 'page-' + str(x)))
    else:
        print('Urls - ' + str(len(urls)))


#поиск всех товаров
def get_item_url():
    for u in urls:
        page_bs = BS(u.content, 'lxml')
        for i in page_bs.select('#catalog_items > .item.b-line > div.w > div.ttl > a'):
            item_url.append(HOST + i.get('href'))
    print('Товаров - ' + str(len(item_url)))


"""def parse(url):
    r = requests.get(url)
    if r:
        print(f'{url} - OK')
        resp.append(r)"""


def item_parse(url):
    print(f'Парсинг товара {url} из {len(item_url)}')
    r = requests.get(url)
    soup = BS(r.content, 'lxml')
    name.append(soup.select('h1.ttl.element__header')[0].string) #Получение названия
    article.append(soup.select('div.article > span.textspan > b')[0].string) #Получение артикула
    price.append(soup.select('div.prices > div.price')[0].string.strip()) #Получение цены
    st = soup.find_all(attrs={'ajax-status': 'PREORDER'}) #Получение статуса
    if len(st) == 0:
        status.append('в наличии')
    else:
        status.append('под заказ')


def excel_write():
    print('Запись данных')
    wb = Workbook()
    ws = wb.active
    ws['A1'] = 'Артикул'
    ws['B1'] = 'Название'
    ws['C1'] = 'Цена'
    ws['D1'] = 'Наличие'
    for i in range(len(article)):
        ws['A' + str(i+2)] = article[i]
        ws['C' + str(i+2)] = price[i]
        ws['B' + str(i+2)] = name[i]
        ws['D' + str(i+2)] = status[i]
    wb.save('parser_rk.xlsx')


def main():
    get_urls()
    get_item_url()
    thread_list = []
    for i in item_url:
        t = threading.Thread(target=item_parse, args=(i,))
        thread_list.append(t)
        t.start()
    for t in thread_list:
        t.join()
    excel_write()
    os.startfile(r'parser_rk.xlsx')

if __name__ == '__main__':
    main()
    print(f'ОТВЕТОВ - {len(resp)}')
