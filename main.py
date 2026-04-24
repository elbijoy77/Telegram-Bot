import telebot

TOKEN = "8604792068:AAG4RPsxyvnTLpWUCjvxXl6FitCsBpdGLvo"
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 7268416193

# ================= DATA =================
balance = {}
pending_deposit = {}
orders = {}

# ================= MENU =================
from telebot.types import ReplyKeyboardMarkup

def menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🛒 অর্ডার", "💳 ডিপোজিট")
    kb.row("📦 অর্ডার স্ট্যাটাস", "👤 আমার একাউন্ট")
    kb.row("📊 দাম ও তথ্য", "🆘 সাপোর্ট")
    return kb

# ================= START =================
@bot.message_handler(commands=['start'])
def start(msg):
    uid = msg.chat.id
    balance.setdefault(uid, 0)

    bot.send_message(
        uid,
        "🏡 স্বাগতম EL SMM ZONE এ\n\nনিচের মেনু থেকে বেছে নিন:",
        reply_markup=menu()
    )

# ================= DEPOSIT =================
@bot.message_handler(func=lambda m: m.text == "💳 ডিপোজিট")
def deposit(msg):
    bot.send_message(msg.chat.id,
        "💳 ডিপোজিট মেথড:\n\n"
        "🟣 bKash: 01819708679\n"
        "🟠 Nagad: 01895288899\n\n"
        "💡 টাকা পাঠিয়ে স্ক্রিনশট পাঠান"
    )

@bot.message_handler(func=lambda m: m.text and m.text.isdigit())
def amount(msg):
    uid = msg.chat.id
    pending_deposit[uid] = int(msg.text)

    bot.send_message(uid, "📸 স্ক্রিনশট পাঠান ডিপোজিট কনফার্ম করার জন্য")

@bot.message_handler(content_types=['photo'])
def photo(msg):
    uid = msg.chat.id

    if uid in pending_deposit:
        amt = pending_deposit[uid]

        bot.send_photo(
            ADMIN_ID,
            msg.photo[-1].file_id,
            caption=f"💰 ডিপোজিট রিকোয়েস্ট\nইউজার: {uid}\nপরিমাণ: {amt}৳\n\nApprove: /add {uid} {amt}"
        )

        bot.send_message(uid, "✅ স্ক্রিনশট পাঠানো হয়েছে")

# ================= ADMIN ADD =================
@bot.message_handler(commands=['add'])
def add(msg):
    if msg.chat.id != ADMIN_ID:
        return

    try:
        _, uid, amt = msg.text.split()
        uid = int(uid)
        amt = int(amt)

        balance[uid] = balance.get(uid, 0) + amt

        bot.send_message(uid, f"✅ আপনার একাউন্টে {amt}৳ যোগ করা হয়েছে")
        bot.send_message(msg.chat.id, "✔ সফলভাবে যোগ হয়েছে")

    except:
        bot.send_message(msg.chat.id, "❌ ব্যবহার করুন: /add user_id amount")

# ================= ORDER =================
@bot.message_handler(func=lambda m: m.text == "🛒 অর্ডার")
def order(msg):
    bot.send_message(msg.chat.id,
        "🛒 অর্ডার দিন:\n\n"
        "ফরম্যাট:\nসার্ভিস - লিংক - পরিমাণ\n\n"
        "উদাহরণ:\nFacebook - link - 100"
    )

@bot.message_handler(func=lambda m: "-" in m.text)
def save_order(msg):
    uid = msg.chat.id
    order_id = len(orders) + 1

    orders[order_id] = {
        "user": uid,
        "data": msg.text,
        "status": "পেন্ডিং"
    }

    bot.send_message(uid, f"📦 অর্ডার হয়েছে!\nঅর্ডার আইডি: {order_id}")

    bot.send_message(
        ADMIN_ID,
        f"📦 নতুন অর্ডার\nআইডি: {order_id}\nইউজার: {uid}\nডাটা: {msg.text}"
    )

# ================= ORDER STATUS =================
@bot.message_handler(func=lambda m: m.text == "📦 অর্ডার স্ট্যাটাস")
def status(msg):
    uid = msg.chat.id

    user_orders = [
        f"আইডি {i} ➜ {o['status']}"
        for i, o in orders.items()
        if o["user"] == uid
    ]

    if not user_orders:
        bot.send_message(uid, "❌ কোনো অর্ডার নেই")
    else:
        bot.send_message(uid, "📦 আপনার অর্ডার:\n\n" + "\n".join(user_orders))

# ================= ACCOUNT =================
@bot.message_handler(func=lambda m: m.text == "👤 আমার একাউন্ট")
def acc(msg):
    uid = msg.chat.id
    bot.send_message(uid, f"💼 আপনার ব্যালেন্স: {balance.get(uid,0)}৳")

# ================= PRICE INFO =================
@bot.message_handler(func=lambda m: m.text == "📊 দাম ও তথ্য")
def price(msg):
    bot.send_message(msg.chat.id,
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "📲 EL SMM ZONE সার্ভিস লিস্ট\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🔵 টেলিগ্রাম\n👁️ ভিউ — ৫ টাকা\n❤️ রিঅ্যাক্ট — ১৫ টাকা\n\n"
        "🔷 ফেসবুক\n👤 ফলোয়ার — ৩০০ টাকা\n\n"
        "🟣 ইনস্টাগ্রাম\n❤️ লাইক — ৫০ টাকা\n\n"
        "⚫ টিকটক\n👍 লাইক — ৩০ টাকা\n\n"
        "🔴 ইউটিউব\n▶️ ভিউ — ৭০ টাকা\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "💡 মিনিমাম অর্ডার: ১০০ টাকা\n"
        "━━━━━━━━━━━━━━━━━━━━━━"
    )

# ================= SUPPORT =================
@bot.message_handler(func=lambda m: m.text == "🆘 সাপোর্ট")
def sup(msg):
    bot.send_message(msg.chat.id, "📞 সাপোর্ট: @BOOM_BHAI")

# ================= RUN =================
print("🔥 EL SMM ZONE BOT RUNNING...")
bot.infinity_polling()
