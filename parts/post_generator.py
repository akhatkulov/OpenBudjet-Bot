def generate_post(cid,card,money):
   payment_text = f"<b> 📑 Foydalanuvchi puli to'lab berildi</b>\n\n\n<b>👤 ID: </b>{cid}\n\n<b>💳 Karta: </b>**** **** **** {card[-4:]}\n\n<b>✍️ Miqdor: </b> {money} so'm\n\n\n<b>🎯 Holat: Muvaffaqiyatli ✅</b>"
   return payment_text