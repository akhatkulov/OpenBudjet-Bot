from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup,ReplyKeyboardRemove
from data.alchemy import get_channel

import conf 
def admin_buttons():
    x = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(text="Statistika", callback_data="stat")
    btn2 = InlineKeyboardButton(text="Xabar yuborish", callback_data="send")
    btn3 = InlineKeyboardButton(text="Kanallarni sozlash", callback_data="channels")
    x.add(btn1, btn2, btn3)
    return x


def channel_control():
    x = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton(text="➕Kanal qo'shish", callback_data="channel_add")
    btn2 = InlineKeyboardButton(text="➖Kanalni olib tashlash", callback_data="channel_del")
    x.add(btn1, btn2)
    return x

def join_key():
    keyboard = InlineKeyboardMarkup(row_width=1)
    x = get_channel()
    r = 1
    for i in x:
        keyboard.add(
            InlineKeyboardButton(f"〽️ {r}-kanal", url=f"https://t.me/{i}")
        )
        r += 1
    keyboard.add(InlineKeyboardButton('✅ Tasdiqlash', callback_data='/start'))
    return keyboard

def home_buttons():
    x = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(text="🗣 OVOZ BERISH",callback_data="give_main_vote")
    btn2 = InlineKeyboardButton(text="💸 HISOBIM",callback_data="show_moneys")
    btn3 = InlineKeyboardButton(text="📣TO'LOVLAR KANALI",url=conf.PAYMENT_CHANNEL_LINK)
    btn4 = InlineKeyboardButton(text="👨‍💻 YORDAM",callback_data="help_center")
    x.add(btn1,btn2,btn3,btn4)
    return x

def vote_buttons():
    x = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(text="🗣 OVOZ BERISH (telegram)",url=conf.BOT_LINK)
    btn2 = InlineKeyboardButton(text="🗣 OVOZ BERISH (sayt)",url=conf.SITE_LINK)
    btn3 = InlineKeyboardButton(text="✅ OVOZ BERDIM",callback_data="vote_submit")
    x.add(btn1,btn2,btn3)
    return x

def back_button():
    x = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(text="🔙 Bosh menyuga qaytish",callback_data="back_home")
    x.add(btn1)
    return x 

def submit_vote_user(cid):
    x = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(text="✅Tasdiqlash",callback_data=f"submit_vote-{cid}")
    x.add(btn1)
    return x 

def receiving_money():
    x = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(text="💳 Pul yechish",callback_data="receiving_money")
    x.add(btn1)
    return x 

def submit_payment(cid,card):
    x = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(text="Tasdiqlash✅",callback_data=f'submit_payment-{cid}-{card}')
    x.add(btn1)
    return x