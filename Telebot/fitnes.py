# coding=utf-8
import telebot
from telebot import types

bot=telebot.TeleBot('1148620994:AAHmVFRnauiAUiKO92VB3aOQRM9LyqYOSsM')

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup2 = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
itembtn0 = types.KeyboardButton('Начать тренировку')
itembtn1 = types.KeyboardButton('Программа 1')
itembtn2 = types.KeyboardButton('Программа 2')
itembtn3 = types.KeyboardButton('Программа 3')
itembtn4 = types.KeyboardButton('Следующая программа')
itembtn5 = types.KeyboardButton('Предыдущая программа')
markup.add(itembtn0)
markup2.add(itembtn1, itembtn2, itembtn3)
markup3.add(itembtn4, itembtn5)

program1 = 'Кардио 30-40 минут в среднем темпе\nЖим лежа - 3 по 15\nРазведение гантелей лежа - 3 по 15\nРазведение гантелей в наклоне - 3 по 20\nЖим штанги или гантелей сидя - 3 по 15\nФранцузкий жим - 2 по 20\nРазгибание рук на блоке стоя - 4 по 20\nПодъем туловища лежа - 3 по 20\nПодъем ног в висе - 2 по 20\nКардио 15-20 минут в среднем, затем в замедленом темпе'
program2 = 'Кардио 30-40 минут\nТяга верхнего блока за голову - 3 по 20\nТяга нижнего блока - 3 по 15\nГиперэкстнзия (разгибание поясницы) - 3 по 20\nПодъем гантелей на бицепс стоя - 2 по 15\nМолот сидя - 2 по 15\nРазведение гантелей через стороны - 2 по 20\nПоднятие гантелей перед собой - 2 по 15\nСкручивание на римском стуле - 3 по 20\nКардио 15-20 минут'
program3 = 'Кардио 30 минут\nПриседания со штангой - 2 по 20\nРазгибание ног в тренажере - 2 по 20\nСгибание ног в тренажере - 2 по 20\nЖим ногами 3 по 20\nПодъём на носки на икры - 5 по 20\nЖим гантелей сидя на плечи - 5 по 20\nРазведение гантелей через стороны - 3 по 15\nСкручивание на римском стуле - 3 по 15\nКардио 10-15 минут'
programs = [program1, program2, program3]
welcome = 'Добро пожаловать.\nДанный бот будет тебе присылать программы тренировок в зале.\nПрограммы расчитаны на посещение зала 3 раза в неделю. Перед началом тренировки выбери нужную программу и приступай к занятиям.\nУдачи!'
print('success')


@bot.message_handler(commands=['start', 'help'])
def start_bot(message):
    bot.send_message(message.chat.id, welcome, reply_markup=markup)

@bot.message_handler(content_types=['text'])
def start_traning(message):
    answer = message.text
    if str(answer) == 'Начать тренировку':
        bot.send_message(message.chat.id, 'Выберите программу', reply_markup=markup2)
    elif str(answer) == 'Программа 1':
        bot.send_message(message.chat.id, programs[0], reply_markup=markup2)
    elif str(answer) == 'Программа 2':
        bot.send_message(message.chat.id, programs[1], reply_markup=markup2)
    elif str(answer) == 'Программа 3':
        bot.send_message(message.chat.id, programs[2], reply_markup=markup2)


bot.polling( none_stop = True )
