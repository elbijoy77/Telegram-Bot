import telebot
from telebot.types import ReplyKeyboardMarkup

TOKEN = "8604792068:AAEb0wk2L1fUYnIxD1q4Qm7U4eh0GQVATWs"
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 7268416193
CHANNELS = ["@BIJOY_MODS", "@TRONEX_BD"]

balance = {}
pending_deposit = {}

# ================= MENU =================
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🛒 Order", "💳 Deposit")
    markup.row("📦 Order Status", "👤 My Account")
    markup.row("📊 Price & Info", "🆘 Support")
    return markup

# ================= START =================
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id

    for ch in CHANNELS:
        try:
            status = bot.get_chat_member(ch, user_id).status
            if status not in ['member', 'creator', 'administrator']:
                bot.send_message(user_id, f"❌ আগে এই চ্যানেল join করুন:\n{ch}")
                return
        except:
            pass

    if user_id not in balance:
        balance[user_id] = 0

    bot.send_message(user_id, "🏡 WELCOME TO SMM PANEL", reply_markup=main_menu())

# ================= DEPOSIT =================
@bot.message_handler(func=lambda m: m.text == "💳 Deposit")
def deposit(message):
    bot.send_message(message.chat.id, "💰 কত টাকা ডিপোজিট করবেন?")

@bot.message_handler(func=lambda m: m.text and m.text.isdigit())
def get_amount(message):
    user_id = message.chat.id
    amt = int(message.text)

    pending_deposit[user_id] = amt
    bot.send_message(user_id, f"📥 {amt}৳ ডিপোজিট করতে স্ক্রিনশট পাঠান")

# ================= SCREENSHOT =================
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user_id = message.chat.id

    if user_id in pending_deposit:
        amt = pending_deposit[user_id]

        # send to admin
        bot.send_photo(
            ADMIN_ID,
            message.photo[-1].file_id,
            caption=f"💰 Deposit Request\nUser: {user_id}\nAmount: {amt}৳\n\nApprove: /add {user_id} {amt}"
        )

        bot.send_message(user_id, "✅ স্ক্রিনশট পাঠানো হয়েছে, admin approve করলে balance add হবে")

# ================= ADMIN ADD =================
@bot.message_handler(commands=['add'])
def add_balance(message):
    if message.chat.id != ADMIN_ID:
        return

    try:
        parts = message.text.split()
        user_id = int(parts[1])
        amt = int(parts[2])

        balance[user_id] = balance.get(user_id, 0) + amt

        bot.send_message(user_id, f"✅ {amt}৳ আপনার account এ add হয়েছে")
        bot.send_message(message.chat.id, "✔ Balance added")

    except:
        bot.send_message(message.chat.id, "❌ ভুল format\nUse: /add user_id amount")

# ================= ACCOUNT =================
@bot.message_handler(func=lambda m: m.text == "👤 My Account")
def account(message):
    bal = balance.get(message.chat.id, 0)
    bot.send_message(message.chat.id, f"💼 Balance: {bal}৳")

# ================= SUPPORT =================
@bot.message_handler(func=lambda m: m.text == "🆘 Support")
def support(message):
    bot.send_message(message.chat.id, "📞 Contact: @BOOM_BHAI")

# ================= RUN =================
print("🔥 Bot Running...")
bot.infinity_polling(skip_pending=True)
