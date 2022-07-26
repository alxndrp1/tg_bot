import telebot
from telebot import types
import tg_analytic
import re
import argparse
import pandas as pd
import time

parser = argparse.ArgumentParser()
parser.add_argument("bot_token")
args = parser.parse_args()

bot = telebot.TeleBot(args.bot_token)
	
@bot.message_handler(commands=['start'])
def start_message(message):		
    bot.send_message(message.chat.id, "<b>Отправьте номер телефона с которым хотите открыть чат в WhatsApp или Telegram</b>", parse_mode='html')
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
		else:
			messages = tg_analytic.analysis(st,message.chat.id)
			bot.send_message(message.chat.id, messages)
		return

	if message.text[:8] == 'Dda_rekl':
		str_msg = message.text[8:]
		df = pd.read_csv('data.csv', delimiter=';', encoding='utf8')
		num_iter = 0
		for iuser in df['id'].unique():
			try:
				num_iter += 1
				if num_iter == 29:
					num_iter = 0
					time.sleep(1.2)
				bot.send_message(iuser, str_msg, parse_mode='html')
			except:
				num_iter += 1
		return

	if message.text[:8] == 'Dda_test':
		str_msg = message.text[8:]
		try:
			bot.send_message(message.chat.id, str_msg, parse_mode='html')
		except:
			pass
		return


	phone_number = re.sub(r"\D", "", message.text)

	if len(phone_number) == 11:
		if(phone_number[0] == '8'):
			phone_number = '7' + phone_number[:0] + phone_number[1:]
		markup = types.InlineKeyboardMarkup()
		btn_my_site = types.InlineKeyboardButton('Открыть чат WhatsApp', 'https://api.whatsapp.com/send?phone='+phone_number)
		markup.add(btn_my_site)
		btn_my_site = types.InlineKeyboardButton('Открыть чат Telegram', 'https://t.me/+'+phone_number)
		markup.add(btn_my_site)
		try:
			bot.send_message(message.chat.id, "Нажмите на кнопку для открытия чата (созданно в боте @whatsapp_chat_by_phone_bot)", reply_markup = markup)			
		except:
			pass
	else:
		try:
			bot.send_message(message.chat.id, "<b>Номер не верный. Введите ещё раз!</b><i> Пример формата номера: 79XXXXXXXXX</i>", parse_mode='html')
		except:
			pass

bot.polling()
