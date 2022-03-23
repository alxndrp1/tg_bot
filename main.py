import telebot
from telebot import types
import tg_analytic
import re
import argparse
import pandas as pd

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

	if message.text[:10] == 'Stasistika':
		st = message.text.split(' ')
		if 'txt' in st or 'тхт' in st:
			tg_analytic.analysis(st,message.chat.id)
			with open('%s.txt' %message.chat.id ,'r',encoding='UTF-8') as file:
				bot.send_document(message.chat.id,file)
			tg_analytic.remove(message.chat.id)
			return
		else:
			messages = tg_analytic.analysis(st,message.chat.id)
			bot.send_message(message.chat.id, messages)
			return

	if message.text[:8] == 'Dda_rekl':
		str_msg = message.text[8:]
		df = pd.read_csv('data.csv', delimiter=';', encoding='utf8')
		for iuser in df['id'].unique():
			try:
				bot.send_message(iuser, str_msg, parse_mode='html')
				return
			except:
				return

	if message.text[:8] == 'Dda_test':
		str_msg = message.text[8:]
		try:
			bot.send_message(message.chat.id, str_msg, parse_mode='html')
			return
		except:
			return

	if re.fullmatch(r'[7]\d{10}', message.text[:11]):
		if message.text[12:16] == 'url':
			try:
				bot.send_message(message.chat.id, 'Открыть чат WhatsApp https://api.whatsapp.com/send?phone='+message.text[:11]+' (созданно в боте @whatsapp_chat_by_phone_bot)', parse_mode='html')
				return
			except:
				return
		markup = types.InlineKeyboardMarkup()
		btn_my_site = types.InlineKeyboardButton('Открыть чат WhatsApp', 'https://api.whatsapp.com/send?phone='+message.text[:11])
		markup.add(btn_my_site)
		try:
			bot.send_message(message.chat.id, "Нажмите на кнопку для открытия чата WhatsApp (созданно в боте @whatsapp_chat_by_phone_bot)", reply_markup = markup)
		except:
			pass
	else:
		try:
			bot.send_message(message.chat.id, "<b>Номер не соответствует необходимому формату. Введите ещё раз!</b>", parse_mode='html')
			bot.send_message(message.chat.id, "<i>Формат номера: 79XXXXXXXXX</i>", parse_mode='html')
		except:
			pass

bot.polling(none_stop=True, interval=1)
