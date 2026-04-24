import telebot

TOKEN = "8604792068:AAG4RPsxyvnTLpWUCjvxXl6FitCsBpdGLvo"
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 7268416193

# ================= DATA =================
balance = {}
pending_deposit = {}
pending_order = {}

# ================= MENU =================
from telebot.types import ReplyKeyboardMarkup

def menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🛒 Order", "💳 Deposit")
    kb.row("👤 My Account", "📦 Order Status")
    kb.row("🆘 Support", "📊 Price Info")
    return kb

# ================= START =================
@bot.message_handler(commands=['start'])
def start(msg):
    uid = msg.chat.id
    if uid not in balance:
        balance[uid] = 0

    bot.send_message(
        uid,
        "🏡 Welcome to Digital Service Panel\n\nChoose an option:",
        reply_markup=menu()
    )

# ================= DEPOSIT =================
@bot.message_handler(func=lambda m: m.text == "💳 Deposit")
def deposit(msg):
    bot.send_message(msg.chat.id, "💰 Enter deposit amount:")

@bot.message_handler(func=lambda m: m.text and m.text.isdigit())
def deposit_amount(msg):
    uid = msg.chat.id
    amt = int(msg.text)

    pending_deposit[uid] = amt
    bot.send_message(uid, f"📥 Send screenshot for {amt} Taka deposit")

# ================= PHOTO (DEPOSIT PROOF) =================
@bot.message_handler(content_types=['photo'])
def photo(msg):
    uid = msg.chat.id

    if uid in pending_deposit:
        amt = pending_deposit[uid]

        bot.send_photo(
            ADMIN_ID,
            msg.photo[-1].file_id,
            caption=f"💰 Deposit Request\nUser: {uid}\nAmount: {amt}\n\nApprove: /add {uid} {amt}"
        )

        bot.send_message(uid, "✅ Screenshot received, waiting for admin approval")

# ================= ADMIN ADD BALANCE =================
@bot.message_handler(commands=['add'])
def add(msg):
    if msg.chat.id != ADMIN_ID:
        return

    try:
        _, uid, amt = msg.text.split()
        uid = int(uid)
        amt = int(amt)

        balance[uid] = balance.get(uid, 0) + amt

        bot.send_message(uid, f"✅ Balance added: {amt} Taka")
        bot.send_message(msg.chat.id, "✔ Done")

    except:
        bot.send_message(msg.chat.id, "❌ Format: /add user_id amount")

# ================= ORDER =================
@bot.message_handler(func=lambda m: m.text == "🛒 Order")
def order(msg):
    bot.send_message(msg.chat.id,
        "🛒 Enter your order details:\nFormat:\nService - Link - Quantity"
    )

@bot.message_handler(func=lambda m: "-" in m.text)
def save_order(msg):
    uid = msg.chat.id
    pending_order[uid] = msg.text

    bot.send_message(uid, "📦 Order received, admin will process it soon")

    bot.send_message(
        ADMIN_ID,
        f"📦 New Order\nUser: {uid}\nDetails: {msg.text}"
    )

# ================= ACCOUNT =================
@bot.message_handler(func=lambda m: m.text == "👤 My Account")
def account(msg):
    uid = msg.chat.id
    bal = balance.get(uid, 0)

    bot.send_message(uid, f"💼 Your Balance: {bal} Taka")

# ================= PRICE INFO =================
@bot.message_handler(func=lambda m: m.text == "📊 Price Info")
def price(msg):
    bot.send_message(msg.chat.id,
        "📊 Service Prices:\n\n"
        "• Basic Service: 10-50 Taka\n"
        "• Standard Service: 50-200 Taka\n"
        "• Premium Service: 200+ Taka\n\n"
        "💡 Minimum order: 100 Taka"
    )

# ================= SUPPORT =================
@bot.message_handler(func=lambda m: m.text == "🆘 Support")
def support(msg):
    bot.send_message(msg.chat.id, "📞 Support: @BOOM_BHAI")

# ================= RUN =================
print("🔥 Bot Running...")
bot.infinity_polling()
