import telebot
from telebot.types import ReplyKeyboardMarkup

TOKEN = "8604792068:AAEb0wk2L1fUYnIxD1q4Qm7U4eh0GQVATWs"
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 7268416193

balance = {}
orders = {}
pending = {}

# ================= MENU =================
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🛒 Order", "💳 Deposit")
    markup.row("📦 Order Status", "👤 My Account")
    markup.row("📊 Price & Info", "🆘 Support")
    return markup

# ================= SERVICES =================
services = {
    "TikTok Likes": 30,
    "TikTok Views": 10,
    "TikTok Followers": 200,

    "Telegram Reaction": 15,
    "Telegram Views": 5,
    "Telegram Subscribers": 30,

    "Facebook Reactions": 70,
    "Facebook Views": 20,
    "Facebook Followers": 300,

    "Instagram Likes": 50,
    "Instagram Views": 5,
    "Instagram Followers": 120,

    "YouTube Likes": 50,
    "YouTube Views": 70,
    "YouTube Subscribers": 100
}

MIN_ORDER = 100

# ================= START =================
@bot.message_handler(commands=['start'])
def start(message):
    uid = message.chat.id
    if uid not in balance:
        balance[uid] = 0

    bot.send_message(uid, f"""
🏡 WELCOME TO SMM PANEL

💰 Balance: {balance[uid]}৳

Choose menu below 👇
""", reply_markup=main_menu())

# ================= ORDER MENU =================
@bot.message_handler(func=lambda m: m.text == "🛒 Order")
def order(message):
    text = "📦 Available Services:\n\n"
    for s, p in services.items():
        text += f"{s} - {p}৳ (Min {MIN_ORDER})\n"

    text += "\n👉 Type service name to order"
    bot.send_message(message.chat.id, text)

# ================= CREATE ORDER =================
@bot.message_handler(func=lambda m: m.text in services.keys())
def create_order(message):
    uid = message.chat.id
    service = message.text
    price = services[service]

    qty = MIN_ORDER  # default minimum order

    total = price

    if balance.get(uid, 0) < total:
        bot.send_message(uid, "❌ Not enough balance")
        return

    balance[uid] -= total

    order_id = len(orders) + 1
    orders[order_id] = {
        "user": uid,
        "service": service,
        "status": "Processing"
    }

    bot.send_message(uid, f"""
✅ Order Placed

Order ID: {order_id}
Service: {service}
Quantity: {qty}
Status: Processing
""")

# ================= ORDER STATUS =================
@bot.message_handler(func=lambda m: m.text == "📦 Order Status")
def status(message):
    uid = message.chat.id

    text = "📦 Your Orders:\n\n"
    found = False

    for oid, data in orders.items():
        if data["user"] == uid:
            text += f"""
Order ID: {oid}
Service: {data['service']}
Status: {data['status']}
------------------
"""
            found = True

    if not found:
        text = "❌ No orders yet"

    bot.send_message(uid, text)

# ================= ACCOUNT =================
@bot.message_handler(func=lambda m: m.text == "👤 My Account")
def account(message):
    uid = message.chat.id
    bot.send_message(uid, f"💰 Balance: {balance.get(uid,0)}৳")

# ================= PRICE INFO =================
@bot.message_handler(func=lambda m: m.text == "📊 Price & Info")
def price(message):
    bot.send_message(message.chat.id, """
📊 SMM PANEL SERVICES

✔ TikTok: Likes / Views / Followers
✔ Telegram: Reaction / Views / Subs
✔ Facebook: React / Views / Followers
✔ Instagram: Likes / Views / Followers
✔ YouTube: Likes / Views / Subscribers

⚠ Min Order: 100
""")

# ================= DEPOSIT =================
@bot.message_handler(func=lambda m: m.text == "💳 Deposit")
def deposit(message):
    bot.send_message(message.chat.id, """
💰 Deposit Method

🟣 bKash: 01819708679
🟠 Nagad: 01895288899

👉 Send Money & send screenshot
""")

# amount
@bot.message_handler(func=lambda m: m.text and m.text.isdigit())
def amount(message):
    pending[message.chat.id] = int(message.text)
    bot.send_message(message.chat.id, "📸 Send payment screenshot")

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
Amount: {amt}

Approve:
/add {uid} {amt}
"""
        )

        bot.send_message(uid, "✅ Sent to admin")

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

        bot.send_message(uid, f"✅ {amt}৳ added")
        bot.send_message(ADMIN_ID, "✔ Done")

    except:
        bot.send_message(ADMIN_ID, "❌ /add user_id amount")

# ================= SUPPORT =================
@bot.message_handler(func=lambda m: m.text == "🆘 Support")
def support(message):
    bot.send_message(message.chat.id, "📞 Contact: @BOOM_BHAI")

# ================= RUN =================
print("Bot Running...")
bot.infinity_polling(skip_pending=True)
