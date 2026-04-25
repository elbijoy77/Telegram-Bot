import telebot

TOKEN = "8604792068:AAG4RPsxyvnTLpWUCjvxXl6FitCsBpdGLvo"
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 7268416193

# ================= DATA =================
balance = {}
pending_deposit = {}
orders = {}
user_step = {}
temp_order = {}

# ================= SERVICES & PRICES =================
services = {
    "1": "Telegram Views",
    "2": "Telegram Reactions",
    "3": "Telegram Subscribers",
    "4": "Facebook Views",
    "5": "Facebook Reacts",
    "6": "Facebook Followers",
    "7": "Instagram Views",
    "8": "Instagram Likes",
    "9": "Instagram Followers",
    "10": "TikTok Views",
    "11": "TikTok Likes",
    "12": "TikTok Followers",
    "13": "YouTube Views",
    "14": "YouTube Likes",
    "15": "YouTube Subscribers"
}

prices = {
    "1": 5, "2": 15, "3": 30,
    "4": 20, "5": 70, "6": 300,
    "7": 5, "8": 50, "9": 120,
    "10": 10, "11": 30, "12": 200,
    "13": 70, "14": 50, "15": 100
}

# ================= MENU =================
from telebot.types import ReplyKeyboardMarkup

def menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🛒 অর্ডার", "💳 ডিপোজিট")
    kb.row("📦 অর্ডার স্ট্যাটাস", "👤 একাউন্ট")
    kb.row("🆘 সাপোর্ট")
    return kb

# ================= START =================
@bot.message_handler(commands=['start'])
def start(msg):
    uid = msg.chat.id
    balance.setdefault(uid, 0)

    bot.send_message(uid,
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "📲 EL SMM ZONE এ স্বাগতম 🚀\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n",
        reply_markup=menu()
    )

# ================= DEPOSIT =================
@bot.message_handler(func=lambda m: m.text == "💳 ডিপোজিট")
def deposit(msg):
    bot.send_message(msg.chat.id,
        "💰 ডিপোজিট পদ্ধতি\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "🟣 বিকাশ: 01819708679\n"
        "🟠 নগদ: 01895288899\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "📸 টাকা পাঠিয়ে স্ক্রিনশট দিন\n"
        "⚠️ মিনিমাম ১০ টাকা"
    )

@bot.message_handler(func=lambda m: m.text and m.text.isdigit())
def amount(msg):
    uid = msg.chat.id
    amt = int(msg.text)

    if amt < 10:
        bot.send_message(uid, "❌ মিনিমাম ১০ টাকা")
        return

    pending_deposit[uid] = amt
    bot.send_message(uid, "📸 এখন স্ক্রিনশট পাঠান")

@bot.message_handler(content_types=['photo'])
def photo(msg):
    uid = msg.chat.id

    if uid in pending_deposit:
        amt = pending_deposit[uid]

        bot.send_photo(
            ADMIN_ID,
            msg.photo[-1].file_id,
            caption=f"💰 Deposit Request\nUser: {uid}\nAmount: {amt}\n\n/add {uid} {amt}"
        )

        bot.send_message(uid, "✅ স্ক্রিনশট পাঠানো হয়েছে")
        del pending_deposit[uid]

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

        bot.send_message(uid, f"✅ {amt}৳ যোগ হয়েছে")
        bot.send_message(msg.chat.id, "✔ Done")

    except:
        bot.send_message(msg.chat.id, "❌ /add user_id amount")

# ================= ORDER MENU =================
@bot.message_handler(func=lambda m: m.text == "🛒 অর্ডার")
def order_menu(msg):
    bot.send_message(msg.chat.id,
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "📲 EL SMM ZONE সার্ভিস লিস্ট 🚀\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"

        "🔵 Telegram\n1. Views\n2. Reactions\n3. Subscribers\n\n"
        "🔷 Facebook\n4. Views\n5. Reacts\n6. Followers\n\n"
        "🟣 Instagram\n7. Views\n8. Likes\n9. Followers\n\n"
        "⚫ TikTok\n10. Views\n11. Likes\n12. Followers\n\n"
        "🔴 YouTube\n13. Views\n14. Likes\n15. Subscribers\n\n"

        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "❓ সার্ভিস নম্বর লিখুন\n⚠️ মিনিমাম 100\n"
        "━━━━━━━━━━━━━━━━━━━━━━"
    )

    user_step[msg.chat.id] = "service"

# ================= ORDER FLOW =================
@bot.message_handler(func=lambda m: True)
def handle(msg):
    uid = msg.chat.id
    text = msg.text

    if uid not in user_step:
        return

    # SERVICE
    if user_step[uid] == "service":

        if text not in services:
            bot.send_message(uid, "❌ ভুল নম্বর")
            return

        temp_order[uid] = {
            "service": services[text],
            "sid": text
        }

        user_step[uid] = "link"
        bot.send_message(uid, "🔗 লিংক দিন")

    # LINK
    elif user_step[uid] == "link":
        temp_order[uid]["link"] = text
        user_step[uid] = "qty"
        bot.send_message(uid, "🔢 পরিমাণ দিন (min 100)")

    # ORDER CREATE
    elif user_step[uid] == "qty":

        if not text.isdigit() or int(text) < 100:
            bot.send_message(uid, "❌ মিনিমাম 100")
            return

        qty = int(text)
        sid = temp_order[uid]["sid"]

        cost = (qty / 1000) * prices[sid]

        if balance.get(uid, 0) < cost:
            bot.send_message(uid, "❌ ব্যালেন্স কম")
            return

        balance[uid] -= cost

        oid = len(orders) + 1

        orders[oid] = {
            "user": uid,
            "service": temp_order[uid]["service"],
            "link": temp_order[uid]["link"],
            "qty": qty,
            "price": cost,
            "status": "Processing"
        }

        bot.send_message(uid,
            f"✅ অর্ডার সফল\nID: {oid}\nCost: {cost}৳"
        )

        bot.send_message(ADMIN_ID,
            f"📥 Order\nID: {oid}\nUser: {uid}\nService: {temp_order[uid]['service']}"
        )

        user_step[uid] = None

# ================= STATUS =================
@bot.message_handler(func=lambda m: m.text == "📦 অর্ডার স্ট্যাটাস")
def status(msg):
    uid = msg.chat.id

    data = [
        f"{i} ➜ {o['service']} ➜ {o['status']}"
        for i, o in orders.items()
        if o["user"] == uid
    ]

    bot.send_message(uid, "\n".join(data) if data else "❌ কোনো অর্ডার নেই")

# ================= ACCOUNT =================
@bot.message_handler(func=lambda m: m.text == "👤 একাউন্ট")
def acc(msg):
    uid = msg.chat.id
    bot.send_message(uid, f"💼 Balance: {balance.get(uid,0)}৳")

# ================= SUPPORT =================
@bot.message_handler(func=lambda m: m.text == "🆘 সাপোর্ট")
def sup(msg):
    bot.send_message(msg.chat.id, "@BOOM_BHAI")

# ================= RUN =================
print("🔥 BOT RUNNING...")
bot.infinity_polling()
