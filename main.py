import telebot
from telebot.types import ReplyKeyboardMarkup

TOKEN = "8604792068:AAEb0wk2L1fUYnIxD1q4Qm7U4eh0GQVATWs"
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 7268416193

balance = {}
pending = {}

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
    uid = message.chat.id
    if uid not in balance:
        balance[uid] = 0

    bot.send_message(uid, f"""
🏡 WELCOME TO SMM PANEL

👤 User ID: {uid}
💰 Balance: {balance[uid]}৳

Menu থেকে অপশন বেছে নিন 👇
""", reply_markup=main_menu())

# ================= PRICE LIST =================
@bot.message_handler(func=lambda m: m.text == "📊 Price & Info")
def price(message):
    bot.send_message(message.chat.id, """
━━━━━━━━━━━━━━━━━━━━━━
📲 EL SMM ZONE – SERVICE LIST
━━━━━━━━━━━━━━━━━━━━━━

🔵 TELEGRAM
👁️ 1K Views — 5 Taka
❤️ 1K Reacts — 15 Taka
👥 1K Members — 30 Taka

🔷 FACEBOOK
🎥 1K Views — 20 Taka
👤 1K Followers — 300 Taka
😍 1K Reactions — 70 Taka

🟣 INSTAGRAM
👁️ 1K Views — 5 Taka
❤️ 1K Likes — 50 Taka
⭐ 1K Followers — 120 Taka

⚫ TIKTOK
👁️ 1K Views — 10 Taka
👍 1K Likes — 30 Taka
⭐ 1K Followers — 200 Taka

🔴 YOUTUBE
👍 1K Likes — 50 Taka
🔔 1K Subscribers — 100 Taka
▶️ 1K Views — 70 Taka

━━━━━━━━━━━━━━━━━━━━━━
""")

# ================= DEPOSIT =================
@bot.message_handler(func=lambda m: m.text == "💳 Deposit")
def deposit(message):
    bot.send_message(message.chat.id, """
💰 DEPOSIT METHOD

━━━━━━━━━━━━━━━━━━
🟣 bKash  →  01819708679
🟠 Nagad  →  01895288899
━━━━━━━━━━━━━━━━━━

💸 কত টাকা ডিপোজিট করবেন? (শুধু সংখ্যা লিখুন)
""")

# amount input
@bot.message_handler(func=lambda m: m.text and m.text.isdigit())
def amount(message):
    uid = message.chat.id
    pending[uid] = int(message.text)
    bot.send_message(uid, "📸 Payment screenshot পাঠান")

# screenshot
@bot.message_handler(content_types=['photo'])
def photo(message):
    uid = message.chat.id

    if uid in pending:
        amt = pending[uid]

        bot.send_photo(
            ADMIN_ID,
            message.photo[-1].file_id,
            caption=f"""
💰 Deposit Request

User: {uid}
Amount: {amt}৳

Approve:
/add {uid} {amt}
"""
        )

        bot.send_message(uid, "✅ Request sent to admin")

# ================= ACCOUNT =================
@bot.message_handler(func=lambda m: m.text == "👤 My Account")
def account(message):
    uid = message.chat.id
    bot.send_message(uid, f"💰 Balance: {balance.get(uid,0)}৳")

# ================= ADMIN ADD =================
@bot.message_handler(commands=['add'])
def add(message):
    if message.chat.id != ADMIN_ID:
        return

    try:
        _, uid, amt = message.text.split()
        uid = int(uid)
        amt = int(amt)

        balance[uid] = balance.get(uid,0) + amt

        bot.send_message(uid, f"✅ {amt}৳ added to your account")
        bot.send_message(ADMIN_ID, "✔ Done")

    except:
        bot.send_message(ADMIN_ID, "❌ Use: /add user_id amount")

# ================= SUPPORT =================
@bot.message_handler(func=lambda m: m.text == "🆘 Support")
def support(message):
    bot.send_message(message.chat.id, "📞 Contact: @BOOM_BHAI")

# ================= RUN =================
print("Bot Running...")
bot.infinity_polling(skip_pending=True)
