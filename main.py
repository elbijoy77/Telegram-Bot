import os
import telebot

TOKEN = os.getenv("8604792068:AAG4RPsxyvnTLpWUCjvxXl6FitCsBpdGLvo")

if not TOKEN:
    print("8604792068:AAG4RPsxyvnTLpWUCjvxXl6FitCsBpdGLvo")
    exit()

bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 7268416193

balance = {}
orders = {}
pending = {}

#========== MENU =================
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🛒 অর্ডার", "💳 ডিপোজিট")
    markup.row("📦 অর্ডার স্ট্যাটাস", "👤 আমার অ্যাকাউন্ট")
    markup.row("📊 প্রাইস ও ইনফো", "🆘 সাপোর্ট")
    return markup

# ================= SERVICE PRICE =================
services = {
    "TikTok Likes": 30,
    "TikTok Views": 10,
    "TikTok Followers": 200,

    "Telegram Reaction": 15,
    "Telegram Views": 5,
    "Telegram Subscriber": 30,

    "Facebook Reaction": 70,
    "Facebook Views": 20,
    "Facebook Followers": 300,

    "Instagram Likes": 50,
    "Instagram Views": 5,
    "Instagram Followers": 120,

    "YouTube Likes": 50,
    "YouTube Views": 70,
    "YouTube Subscriber": 100
}

MIN_ORDER = 100

# ================= START =================
@bot.message_handler(commands=['start'])
def start(message):
    uid = message.chat.id

    if uid not in balance:
        balance[uid] = 0

    bot.send_message(uid, f"""
🏡 স্বাগতম EL SMM ZONE 🚀

👋 হ্যালো!
💰 আপনার ব্যালেন্স: {balance[uid]}৳

📲 নিচের মেনু থেকে নির্বাচন করুন 👇
""", reply_markup=main_menu())

# ================= ORDER =================
@bot.message_handler(func=lambda m: m.text == "🛒 অর্ডার")
def order(message):
    bot.send_message(message.chat.id, """
━━━━━━━━━━━━━━━━━━━━━━
📲 EL SMM ZONE সার্ভিস লিস্ট
━━━━━━━━━━━━━━━━━━━━━━

🔵 টেলিগ্রাম
👁️ ভিউ | ❤️ রিঅ্যাকশন | 👥 সাবস্ক্রাইবার

🔷 ফেসবুক
🎥 ভিউ | 😍 রিঅ্যাক্ট | 👤 ফলোয়ার

🟣 ইনস্টাগ্রাম
👁️ ভিউ | ❤️ লাইক | ⭐ ফলোয়ার

⚫ টিকটক
👁️ ভিউ | 👍 লাইক | ⭐ ফলোয়ার

🔴 ইউটিউব
▶️ ভিউ | 👍 লাইক | 🔔 সাবস্ক্রাইবার

━━━━━━━━━━━━━━━━━━━━━━

⚠️ মিনিমাম অর্ডার: 100 থেকে শুরু
👉 সার্ভিসের নাম লিখে অর্ডার করুন
""")

# ================= CREATE ORDER =================
@bot.message_handler(func=lambda m: m.text in services.keys())
def create_order(message):
    uid = message.chat.id
    service = message.text
    price = services[service]

    if balance.get(uid, 0) < price:
        bot.send_message(uid, "❌ দুঃখিত! আপনার পর্যাপ্ত ব্যালেন্স নেই 😢")
        return

    balance[uid] -= price

    order_id = len(orders) + 1
    orders[order_id] = {
        "user": uid,
        "service": service,
        "status": "প্রসেসিং ⏳"
    }

    bot.send_message(uid, f"""
━━━━━━━━━━━━━━
✅ অর্ডার সফল হয়েছে 🎉
━━━━━━━━━━━━━━

🆔 অর্ডার আইডি: {order_id}
📦 সার্ভিস: {service}
💰 মূল্য: {price}৳
⏳ স্ট্যাটাস: প্রসেসিং

🙏 ধন্যবাদ আমাদের সাথে থাকার জন্য!
""")

# ================= ORDER STATUS =================
@bot.message_handler(func=lambda m: m.text == "📦 অর্ডার স্ট্যাটাস")
def status(message):
    uid = message.chat.id

    text = "📦 আপনার অর্ডারসমূহ 👇\n\n"
    found = False

    for oid, data in orders.items():
        if data["user"] == uid:
            text += f"""
🆔 আইডি: {oid}
📦 {data['service']}
⏳ স্ট্যাটাস: {data['status']}
━━━━━━━━━━━━━━
"""
            found = True

    if not found:
        text = "❌ কোনো অর্ডার পাওয়া যায়নি 😢"

    bot.send_message(uid, text)

# ================= ACCOUNT =================
@bot.message_handler(func=lambda m: m.text == "👤 আমার অ্যাকাউন্ট")
def account(message):
    uid = message.chat.id

    bot.send_message(uid, f"""
👤 অ্যাকাউন্ট তথ্য

🆔 আইডি: {uid}
💰 ব্যালেন্স: {balance.get(uid,0)}৳

🙏 EL SMM ZONE ব্যবহার করার জন্য ধন্যবাদ
""")

# ================= PRICE INFO =================
@bot.message_handler(func=lambda m: m.text == "📊 প্রাইস ও ইনফো")
def price(message):
    bot.send_message(message.chat.id, """
━━━━━━━━━━━━━━━━━━━━━━
📲 EL SMM ZONE সার্ভিস লিস্ট
━━━━━━━━━━━━━━━━━━━━━━

🔵 টেলিগ্রাম
👁️ 1K ভিউ — 5 টাকা
❤️ 1K রিঅ্যাকশন — 15 টাকা
👥 1K সাবস্ক্রাইবার — 30 টাকা

🔷 ফেসবুক
🎥 1K ভিউ — 20 টাকা
👤 1K ফলোয়ার — 300 টাকা
😍 1K রিঅ্যাকশন — 70 টাকা

🟣 ইনস্টাগ্রাম
👁️ 1K ভিউ — 5 টাকা
❤️ 1K লাইক — 50 টাকা
⭐ 1K ফলোয়ার — 120 টাকা

⚫ টিকটক
👁️ 1K ভিউ — 10 টাকা
👍 1K লাইক — 30 টাকা
⭐ 1K ফলোয়ার — 200 টাকা

🔴 ইউটিউব
👍 1K লাইক — 50 টাকা
🔔 1K সাবস্ক্রাইবার — 100 টাকা
▶️ 1K ভিউ — 70 টাকা

━━━━━━━━━━━━━━━━━━━━━━

⚠️ মিনিমাম অর্ডার: 100 থেকে শুরু
🔥 দ্রুত ডেলিভারি
""")

# ================= DEPOSIT =================
@bot.message_handler(func=lambda m: m.text == "💳 ডিপোজিট")
def deposit(message):
    bot.send_message(message.chat.id, """
💰 ডিপোজিট পদ্ধতি

━━━━━━━━━━━━━━━━━━
🟣 বিকাশ: 01819708679
🟠 নগদ: 01895288899
━━━━━━━━━━━━━━━━━━

📸 টাকা পাঠিয়ে স্ক্রিনশট দিন
💬 অ্যাডমিন approve করবে
""")

# amount
@bot.message_handler(func=lambda m: m.text and m.text.isdigit())
def amount(message):
    pending[message.chat.id] = int(message.text)
    bot.send_message(message.chat.id, "📸 স্ক্রিনশট পাঠান")

# photo
@bot.message_handler(content_types=['photo'])
def photo(message):
    uid = message.chat.id

    if uid in pending:
        amt = pending[uid]

        bot.send_photo(
            ADMIN_ID,
            message.photo[-1].file_id,
            caption=f"""
💰 নতুন ডিপোজিট রিকোয়েস্ট

👤 ইউজার: {uid}
💵 পরিমাণ: {amt}৳

👉 অনুমোদন:
/add {uid} {amt}
"""
        )

        bot.send_message(uid, "✅ রিকোয়েস্ট পাঠানো হয়েছে")

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

        bot.send_message(uid, f"🎉 {amt}৳ যোগ করা হয়েছে!")
        bot.send_message(ADMIN_ID, "✔ সম্পন্ন")

    except:
        bot.send_message(ADMIN_ID, "❌ /add user_id amount")
#================= SUPPORT =================
@bot.message_handler(func=lambda m: m.text == "🆘 সাপোর্ট")
def support(message):
    bot.send_message(message.chat.id, "📞 যোগাযোগ: @BOOM_BHAI")

# ================= RUN =================
print("🔥 EL SMM ZONE Bot চালু হয়েছে...")
bot.infinity_polling(skip_pending=True)
