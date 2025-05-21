import telebot
import re

BOT_TOKEN = "7947971723:AAF337weeQ8EAI5f6-Qw9pYA_RZr_i-eaqM"
ADMIN_CHAT_ID = 1080210626

bot = telebot.TeleBot(BOT_TOKEN)
user_data = {}

@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Assalomu alaykum, AKITA University ga hujjat topshirishni istaysizmi? (Ha/Yo‘q)")
    user_data[chat_id] = {"step": "confirm"}

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text.strip()

    if chat_id not in user_data:
        bot.send_message(chat_id, "Iltimos, /start buyrug'ini yuboring.")
        return

    step = user_data[chat_id]["step"]

    if step == "confirm":
        if text.lower() == "ha":
            user_data[chat_id]["step"] = "lastname"
            bot.send_message(chat_id, "Familiyangizni kiriting:")
        elif text.lower() in ["yo'q", "yo‘q"]:
            bot.send_message(chat_id, "Yaxshi, kerak bo‘lsa /start bilan qayta boshlang.")
            user_data.pop(chat_id)
        else:
            bot.send_message(chat_id, "Iltimos, faqat 'Ha' yoki 'Yo‘q' deb javob bering.")

    elif step == "lastname":
        if not text.isalpha():
            bot.send_message(chat_id, "Familiya faqat harflardan iborat bo‘lishi kerak. Qaytadan kiriting:")
            return
        user_data[chat_id]["lastname"] = text
        user_data[chat_id]["step"] = "firstname"
        bot.send_message(chat_id, "Ismingizni kiriting:")

    elif step == "firstname":
        if not text.isalpha():
            bot.send_message(chat_id, "Ism faqat harflardan iborat bo‘lishi kerak. Qaytadan kiriting:")
            return
        user_data[chat_id]["firstname"] = text
        user_data[chat_id]["step"] = "age"
        bot.send_message(chat_id, "Yoshingizni kiriting:")

    elif step == "age":
        if not text.isdigit():
            bot.send_message(chat_id, "Iltimos, yoshi raqam bilan kiriting:")
            return
        user_data[chat_id]["age"] = text
        user_data[chat_id]["step"] = "passport"
        bot.send_message(chat_id, "Passport raqamingizni kiriting (masalan: AD1234567):")

    elif step == "passport":
        if not re.match(r"^[A-Z]{2}\d{7}$", text):
            bot.send_message(chat_id, "Noto‘g‘ri passport raqam! Masalan: AD1234567 (2 harf + 7 raqam). Qaytadan kiriting:")
            return
        user_data[chat_id]["passport"] = text
        user_data[chat_id]["step"] = "phone"
        bot.send_message(chat_id, "Telefon raqamingizni kiriting (masalan: +998901234567):")

    elif step == "phone":
        if not re.match(r"^\+998\d{9}$", text):
            bot.send_message(chat_id, "Noto‘g‘ri format! Telefon raqam +998 bilan boshlanib, jami 13 ta belgidan iborat bo‘lishi kerak. Qaytadan kiriting:")
            return
        user_data[chat_id]["phone"] = text

        # Tasdiqlash xabari
        bot.send_message(chat_id,
                         f"Hujjat topshirildi ✅\n\n"
                         f"👤 F.I.Sh: {user_data[chat_id]['lastname']} {user_data[chat_id]['firstname']}\n"
                         f"🎂 Yosh: {user_data[chat_id]['age']}\n"
                         f"🛂 Passport: {user_data[chat_id]['passport']}\n"
                         f"📞 Telefon: {user_data[chat_id]['phone']}\n\n"
                         f"Tez orada siz bilan bog'lanamiz.")

        # Admin uchun xabar
        admin_msg = (
            f"Yangi hujjat topshirildi!\n\n"
            f"👤 F.I.Sh: {user_data[chat_id]['lastname']} {user_data[chat_id]['firstname']}\n"
            f"🎂 Yosh: {user_data[chat_id]['age']}\n"
            f"🛂 Passport: {user_data[chat_id]['passport']}\n"
            f"📞 Telefon: {user_data[chat_id]['phone']}\n"
            f"Telegram ID: {chat_id}"
        )
        bot.send_message(ADMIN_CHAT_ID, admin_msg)

        user_data.pop(chat_id)

if __name__ == "__main__":
    bot.remove_webhook()  # Agar webhook faol bo'lsa, uni o'chirib qo'yadi
    bot.polling(none_stop=True)
