import telebot
from telebot import types
import tg_analytic
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("bot_token")
args = parser.parse_args()

bot = telebot.TeleBot(args.bot_token)
	
@bot.message_handler(commands=['start'])
def start_message(message):		
    bot.send_message(message.chat.id, "<b>Отправьте номер телефона с которым хотите открыть чат в WhatsApp</b>", parse_mode='html')
    bot.send_message(message.chat.id, "<i>Формат номера: 79XXXXXXXXX</i>", parse_mode='html')
    tg_analytic.statistics(message.chat.id, message.text)

@bot.message_handler(content_types=['text'])
def send_text(message):
	tg_analytic.statistics(message.chat.id, message.text)
	if re.fullmatch(r'[7]\d{10}', message.text):
		markup = types.InlineKeyboardMarkup()
		btn_my_site = types.InlineKeyboardButton('Открыть чат WhatsApp', 'https://api.whatsapp.com/send?phone='+message.text)
		markup.add(btn_my_site)
		bot.send_message(message.chat.id, "Нажмите на кнопку для открытия чата WhatsApp", reply_markup = markup)
	else:
		bot.send_message(message.chat.id, "<b>Номер не соответствует необходимому формату. Введите ещё раз!</b>", parse_mode='html')
		bot.send_message(message.chat.id, "<i>Формат номера: 79XXXXXXXXX</i>", parse_mode='html')

	if message.text[:10] == 'Stasistika':
		st = message.text.split(' ')
		if 'txt' in st or 'тхт' in st:
			tg_analytic.analysis(st,message.chat.id)
			with open('%s.txt' %message.chat.id ,'r',encoding='UTF-8') as file:
				bot.send_document(message.chat.id,file)
			tg_analytic.remove(message.chat.id)
		else:
			messages = tg_analytic.analysis(st,message.chat.id)
			bot.send_message(message.chat.id, messages)

bot.polling(none_stop=True, interval=1)
