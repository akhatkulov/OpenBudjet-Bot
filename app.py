import telebot

from data.alchemy import create_user, get_step, put_step, user_count, get_all_user, \
    get_channel, put_channel, get_channel_with_id, delete_channel,check_number,get_money,add_money,claim_money

from helper.buttons import admin_buttons,channel_control,join_key,home_buttons,vote_buttons,back_button,submit_vote_user,receiving_money,submit_payment
from parts.post_generator import generate_post
import conf

bot = telebot.TeleBot(conf.BOT_TOKEN, parse_mode="html")

admin_id = conf.ADMIN_ID

def join(user_id):
    try:
        xx = get_channel()
        r = 0
        for i in xx:
            res = bot.get_chat_member(f"@{i}", user_id)
            x = ['member', 'creator', 'administrator']
            if res.status in x:
                r += 1
        if r != len(xx):
            bot.send_message(user_id,
                             "<b>👋 Assalomu alaykum Botni ishga tushurish uchun kanallarga a'zo bo'ling va a'zolikni tekshirish buyrug'ini bosing.</b>",
                             parse_mode='html', reply_markup=join_key())
            return False
        else:
            return True
    except Exception as e:
        bot.send_message(chat_id=admin_id, text=f"Kanalga bot admin qilinmagan yoki xato: {str(e)}")
        return True


@bot.message_handler(commands=['start'])
def start(message):
    if message.text == "/start" and join(message.chat.id):

        bot.send_message(message.chat.id,f"<b>💸Pul ishlash  uchun «🗣 Ovoz berish» tugmasini bosib, ovoz bering ✅</b>",parse_mode='html',reply_markup=home_buttons())
        try:
            create_user(cid=message.chat.id,name=message.chat.first_name)
        except Exception as e:
            print(f"Error creating user: {str(e)}")

        
@bot.message_handler(content_types=['text'])
def more(message):
    if message.text == "/admin" and message.chat.id == admin_id:
        bot.send_message(chat_id=admin_id, text="Salom, Admin", reply_markup=admin_buttons())
        put_step(cid=message.chat.id, step="!!!")

    if get_step(message.chat.id) == "channel_del" and message.text != "/start" and message.text != "/admin":
        x = int(message.text)
        if delete_channel(ch_id=x):
            bot.send_message(chat_id=message.chat.id, text="Kanal olib tashlandi")
            put_step(cid=message.chat.id, step="!!!")
        else:
            bot.send_message(chat_id=message.chat.id, text="Xatolik! IDni to'g'ri kiritdingizmi tekshiring!")

    if get_step(message.chat.id) == "add_channel" and message.text != "/start" and message.text != "/admin":
        if put_channel(message.text):
            bot.send_message(chat_id=message.chat.id, text=f"{message.text} kanali qabul qilindi!")
            put_step(cid=int(admin_id), step="!!!")
        else:
            bot.send_message(chat_id=message.chat.id,
                             text="Xatolik! Bu kanal oldin qo'shilgan bo'lishi mumkin yoki boshqa xatolik, iltimos tekshiring")
            put_step(cid=int(admin_id), step="!!!")
    
    if get_step(message.chat.id) == 'send':
        text = message.text
        mid = message.id
        bot.send_message(chat_id=message.chat.id, text="Xabar yuborish boshlandi")
        try:
            for i in get_all_user():
                try:
                    bot.forward_message(chat_id=i, from_chat_id=admin_id, message_id=mid)
                except Exception as e:
                    print(f"Error sending message to user {i}: {str(e)}")
            bot.send_message(chat_id=message.chat.id, text="Tarqatish yakunlandi")
            put_step(cid=int(admin_id), step="!!!")
        except Exception as e:
            bot.send_message(chat_id=message.chat.id, text=f"Xabar yuborishda muammo bo'ldi: {str(e)}")
    
    if get_step(message.chat.id) == 'get_vote_number':
        if len(message.text) == 13 :
            if check_number(number=message.text):
                bot.send_message(chat_id=admin_id,text=f"<b>Foydalanuvchi tekshiriv uchun so'rov yubordi.\nOvoz bergan raqam:</b> {message.text}",reply_markup=submit_vote_user(cid=message.chat.id))
                bot.send_message(chat_id=message.chat.id,text="Raqamingiz tekshirish uchun adminga yuborildi✅",reply_markup=back_button())
            else:
                bot.send_message(chat_id=message.chat.id,text="Bu raqamdan oldin ovoz berilgan🚫",reply_markup=back_button())
        else:
            bot.send_message(chat_id=message.chat.id,text="Noto'g'ri raqam, +998901231212 ko'rinishida kiriting",reply_markup=back_button())
    
    if get_step(message.chat.id) == 'receiving_money':
        bot.send_message(chat_id=message.chat.id,text=f"{get_money(cid=message.chat.id)} so'm to'lov uchun yuborildi. Hisobotlar: <a href='{conf.PAYMENT_CHANNEL_LINK}'>LINK</a>",parse_mode="html")
        bot.send_message(chat_id=admin_id,text=f"<b>Foydalanuvchi pul yechmoqchi!\nKarta raqami:</b> <code> {message.text} </code>\nBalansi: {get_money(cid=message.chat.id)}",reply_markup=submit_payment(cid=message.chat.id,card=message.text))
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):  
    if call.data == "/start" and join(call.message.chat.id):
        bot.send_message(chat_id=call.message.chat.id,text="<b>Obuna tasdiqlandi✅</b>",parse_mode="html") 
    if call.data == "stat" and str(call.message.chat.id) == str(admin_id):
        bot.send_message(chat_id=call.message.chat.id, text=f"Foydalanuvchilar soni: {user_count()}")
    if call.data == "send" and str(call.message.chat.id) == str(admin_id):
        put_step(cid=call.message.chat.id, step="send")
        bot.send_message(chat_id=call.message.chat.id, text="Forward xabaringizni yuboring")
    if call.data == "channels" and str(call.message.chat.id) == str(admin_id):
        r = get_channel_with_id()
        bot.send_message(chat_id=call.message.chat.id, text=f"Kanallar ro'yxati:{r}", reply_markup=channel_control())
    if call.data == "channel_add" and str(call.message.chat.id) == str(admin_id):
        put_step(cid=call.message.chat.id, step="add_channel")
        bot.send_message(chat_id=call.message.chat.id, text="Kanali linkini yuboring! bekor qilish uchun /start !")
    if call.data == "channel_del" and str(call.message.chat.id) == str(admin_id):
        put_step(cid=call.message.chat.id, step="channel_del")
        bot.send_message(chat_id=call.message.chat.id,
                         text=f"{get_channel_with_id()}\n⚠️O'chirmoqchi bo'lgan kanalingiz IDsini bering, bekor qilish uchun /start yoki /admin deng!")

    if call.data == "help_center":
        bot.send_message(
            chat_id=call.message.chat.id,
            text=f"<b>To'lovlar kanali:</b> <a href='{conf.PAYMENT_CHANNEL_LINK}'>Payment Channel</a>\n<b>ADMIN:</b> {conf.SUPPORT_USERNAME}",
            parse_mode="html"
        )   
    if call.data == "give_main_vote":
        main_vote = f"""❗️Ovoz berish jarayoni muvaffaqiyatli yakunlangach, hisobingizga avtomatik tarzda  1ta ovozga {conf.VOTE_PAYMENT_SUM}  pul mablag'i o'tkaziladi!

Diqqat! Ovoz bermasdan turib <b>"✅ Ovoz berdim"</b> tugmasini bossangiz, botdan bloklanasiz!"""
        bot.send_message(chat_id=call.message.chat.id,text=main_vote,reply_markup=vote_buttons(),parse_mode="html")
    
    if call.data == "vote_submit":
        bot.send_message(chat_id=call.message.chat.id,text="Ovoz bergan raqamingizni yuboring")
        put_step(cid=call.message.chat.id,step="get_vote_number")
    
    if call.data == "back_home":
        put_step(cid=call.message.chat.id,step="!!!")
        bot.send_message(call.message.chat.id,f"<b>💸Pul ishlash  uchun «🗣 Ovoz berish» tugmasini bosib, ovoz bering ✅</b>",parse_mode='html',reply_markup=home_buttons())
    
    if call.data == "show_moneys":
        moneys = get_money(cid=call.message.chat.id)
        bot.send_message(chat_id=call.message.chat.id,text=f"<b>Hisobingiz:</b> {moneys} so'm",parse_mode="html",reply_markup=receiving_money())

    if "submit_vote" in call.data:
        check_user_id = call.data.split("-")[1]
        add_money(cid=call.message.chat.id,payment_money=conf.VOTE_PAYMENT_SUM)
        bot.send_message(chat_id=call.message.chat.id,text="Bajarildi✅")
        bot.send_message(chat_id=check_user_id,text=f"Ovozingiz qabul qilindi. Hisobingiz <b>{conf.VOTE_PAYMENT_SUM} so'm </b>ga to'ldirildi",parse_mode="html",reply_markup=back_button())

    if call.data == "receiving_money":
        if get_money(cid=call.message.chat.id)>=conf.MIN_PAYMENT:
            put_step(cid=call.message.chat.id,step="receiving_money")
            bot.send_message(chat_id=call.message.chat.id,text="Karta raqam kiriting:")
        else:
            bot.send_message(chat_id=call.message.chat.id,text=f"<b>💳Hisobingizda mablag' yetarli emas!\nEng kam oul yechish miqdori: </b>{conf.MIN_PAYMENT}",parse_mode="html")

    if "submit_payment" in call.data:
        payment_user_id = call.data.split("-")[1]
        payment_card = call.data.split("-")[2]
        money_x = get_money(cid=call.message.chat.id)
        claim_money(cid=int(payment_user_id))
        bot.send_message(chat_id=payment_user_id,text="Pul hisobingizga tushdi✅",reply_markup=back_button())
        bot.send_message(chat_id=admin_id,text="O'tkazma tasdiqlandi✅")
        bot.send_message(chat_id=conf.PAYMENT_CHANNEL_ID,text=generate_post(cid=payment_user_id,card=payment_card,money=money_x))
        
if __name__ == '__main__':
    print(bot.get_me())
    bot.polling(none_stop=True)
