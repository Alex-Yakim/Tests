import requests
from bs4 import BeautifulSoup as BS
from openpyxl import Workbook


class ParserInRed():
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
        }
        self.HOST = 'https://inredhome.ru'
        self.wb = Workbook()
        self.ws = self.wb.active

    def check_image(self, url):
        """Проверяет, есть ли фото в карточке товара.
            Если есть, возращает True, иначе False"""
        r = self.session.get(url)
        soup = BS(r.content, 'lxml')
        div_image = soup.select('div.tovar_img > div > div > div.custom-slider__detail-wraper')
        a_tag = div_image[0].find('a')
        href = a_tag.get('href')
        no_image_url = '/bitrix/templates/in_red_mobmenu/components/bitrix/catalog/catalog-inred3/bitrix/catalog.element/.default/images/no_photo.png'
        if href == no_image_url:
            return False
        else:
            return True

    def get_catalog_links(self, url):
        """Собирает ссылки на разделы каталога
            и возвращает их список"""
        # r = self.session.get(self.HOST + '/catalog/')
        r = self.session.get(url)
        soup = BS(r.content, 'lxml')
        div_item = soup.select('div.section_list > div.item > div > div.name > a')
        hrefs = []
        for item in div_item:
            hrefs.append(f"{self.HOST}{item.get('href')}")
        return hrefs

    def get_pagination(self, url):
        """Возвращает количество страниц с товаром"""
        r = self.session.get(url)
        soup = BS(r.content, 'lxml')
        pagination = soup.select('#pagination > li')
        if pagination:
            max_page = pagination[-1].a.text
            return int(max_page)
        else:
            return 1

    def get_item_url_and_check(self, url, page: int):
        params = {'PAGEN_4': page}
        r = self.session.get(url, params=params)
        soup = BS(r.content, 'lxml')
        div_item = soup.select('div.products__container.js_ct_product_container > div.products__item > a')
        hrefs = []
        for item in div_item:
            hrefs.append(f"{self.HOST}{item.get('href')}")
        for item_url in hrefs:
            if not self.check_image(item_url):
                print(item_url)
                self.write_excel(item_url)

    def write_excel(self, url):
        self.ws.insert_rows(2)
        self.ws['A2'] = url
        self.wb.save('no_photo.xlsx')

    def start(self):
        catalog_urls = list(self.get_catalog_links(url=self.HOST + '/catalog/'))
        for url in catalog_urls:
            print(url)
            for i in range(1, self.get_pagination(url) + 1):
                print(f'Страница {i}')
                self.get_item_url_and_check(url=url, page=i)


if __name__ == '__main__':
    parser = ParserInRed()
    parser.start()
    # for url in parser.test_urls:
    #     if not parser.check_image(url):
    #         print(url)

    # catalog_url = list(parser.get_catalog_links('https://inredhome.ru/catalog/'))
    # for u in catalog_url:
    #     print(f'{u} - страниц {parser.get_pagination(u)}')

    # parser.get_pagination('https://inredhome.ru/catalog/oborudovanie_dlya_vodosnabzheniya/')

    # url = 'https://inredhome.ru/catalog/oborudovanie_dlya_vodosnabzheniya/'
    # for i in range(parser.get_pagination(url), 0, -1):
    #     print(f'Страница {i}')
        # parser.get_item_url_and_check('https://inredhome.ru/catalog/oborudovanie_dlya_vodosnabzheniya/', i)
        # print(i)
