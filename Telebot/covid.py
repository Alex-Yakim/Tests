import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup as BS

bot=telebot.TeleBot('1019462667:AAHMW6MtqSDJlictfCIyo3vV3zWCYzr7ToQ')

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
itembtn1 = types.KeyboardButton('Получить данные')
markup.add(itembtn1)

def cbr_euro():
    r = requests.get('https://www.cbr.ru/')
    soup = BS(r.content, 'lxml')
    euro = soup.select('#content > div > div > div > div > div.indicators.home-indicators.d-none.d-md-block > div.row.home-indicators_items > div:nth-child(3) > div > div:nth-child(2) > div > div:nth-child(3) > div')
    return euro[0].text

def cbr_dollar():
    r = requests.get('https://www.cbr.ru/')
    soup = BS(r.content, 'lxml')
    dollar = soup.select('#content > div > div > div > div > div.indicators.home-indicators.d-none.d-md-block > div.row.home-indicators_items > div:nth-child(3) > div > div:nth-child(1) > div > div:nth-child(3) > div')
    return dollar[0].text

def covid_ekb():
    #r = requests.Session()
    r = requests.get('https://coronavirus-monitor.info/country/russia/sverdlovskaya-oblast/', headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'})
    soup = BS(r.content, 'lxml')
    div = soup.find_all('div', class_='col-md-4 text-center')
    return div

def covid_rus():
    r = requests.get('https://coronavirus-monitor.info/country/russia/')
    soup = BS(r.content, 'lxml')
    div = soup.find_all('div', class_='col-md-4 text-center')
    return div

def covid_world():
    r = requests.get('https://coronavirus-monitor.info/')
    soup = BS(r.content, 'lxml')
    div = soup.select('#content > div.container.content > div > div.col-xs-12.col-sm-12.col-md-9.col-lg-9 > div.row.justify-content-center > div:nth-child(1) > div > h2')
    return div

@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id, 'Нажмите "Получить данные"', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_data(message):
    answer = message.text
    if str(answer) == 'Получить данные':

        bot.send_message(message.chat.id, 'Статистика коронавируса в Свердловской области\n\n'+ covid_ekb()[0].text.replace('Заражено', 'Заражено ').strip() + '\n' + covid_ekb()[1].text.replace('Вылечено', 'Вылечено  ').strip() + '\n' + covid_ekb()[2].text.replace('Погибло', 'Погибло ').strip(), reply_markup=markup)
        bot.send_message(message.chat.id, 'Статистика коронавируса в России\n\n'+ covid_rus()[0].text.replace('Заражено', 'Заражено ').strip() + '\n' + covid_rus()[1].text.replace('Вылечено', 'Вылечено ').strip() + '\n' + covid_rus()[2].text.replace('Погибло', 'Погибло ').strip() + '\n\nВсего в мире\n' + covid_world()[0].text.replace('Заражено', 'Заражено '), reply_markup=markup)
        bot.send_message(message.chat.id, 'Курс евро - ' + cbr_euro() + '\nКурс доллара - ' + cbr_dollar(), reply_markup=markup)

bot.polling( none_stop = True )
