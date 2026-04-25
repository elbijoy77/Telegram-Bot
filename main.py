import telebot
from telebot.types import ReplyKeyboardMarkup

TOKEN = "8604792068:AAG4RPsxyvnTLpWUCjvxXl6FitCsBpdGLvo"
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 7268416193

balance = {}
orders = {}
pending = {}

# ================= MENU =================
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🛒 অর্ডার", "💳 ডিপোজিট")
    markup.row("📦 অর্ডার স্ট্যাটাস", "👤 আমার অ্যাকাউন্ট")
    markup.row("📊 প্রাইস ও ইনফো", "🆘 সাপোর্ট")
    return markup


#================= START =================
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

# ================= SERVICE MENU =================

@bot.message_handler(func=lambda m: m.text == "🛒 অর্ডার")
def order_menu(msg):
    bot.send_message(msg.chat.id,
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "📲 EL SMM ZONE – SERVICE LIST 🚀\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"

        "🔵 টেলিগ্রাম সার্ভিস\n"
        "1. 📈 Telegram Views\n"
        "2. ❤️ Telegram Reactions\n"
        "3. 👥 Telegram Subscribers\n\n"

        "🔷 ফেসবুক সার্ভিস\n"
        "4. 🎥 Facebook Views\n"
        "5. 😍 Facebook Reacts\n"
        "6. 👤 Facebook Followers\n\n"

        "🟣 ইনস্টাগ্রাম সার্ভিস\n"
        "7. 👁️ Instagram Views\n"
        "8. ❤️ Instagram Likes\n"
        "9. ⭐ Instagram Followers\n\n"

        "⚫ টিকটক সার্ভিস\n"
        "10. 👁️ TikTok Views\n"
        "11. 👍 TikTok Likes\n"
        "12. ⭐ TikTok Followers\n\n"

        "🔴 ইউটিউব সার্ভিস\n"
        "13. ▶️ YouTube Views\n"
        "14. 👍 YouTube Likes\n"
        "15. 🔔 YouTube Subscribers\n\n"

        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "❓ সার্ভিস নম্বর লিখুন\n"
        "⚠️ মিনিমাম অর্ডার: 100\n"
        "━━━━━━━━━━━━━━━━━━━━━━"
    )

    user_step[msg.chat.id] = "service"


# ================= ORDER FLOW =================

@bot.message_handler(func=lambda m: True)
def handle_order(msg):
    uid = msg.chat.id
    text = msg.text

    if uid not in user_step:
        return

    # STEP 1: SERVICE SELECT
    if user_step[uid] == "service":

        if text not in services:
            bot.send_message(uid, "❌ ভুল সার্ভিস নম্বর")
            return

        temp_order[uid] = {
            "service": services[text],
            "sid": text
        }

        user_step[uid] = "link"
        bot.send_message(uid, "🔗 আপনার লিংক দিন")

    # STEP 2: LINK
    elif user_step[uid] == "link":

        temp_order[uid]["link"] = text
        user_step[uid] = "qty"

        bot.send_message(uid, "🔢 পরিমাণ লিখুন (মিনিমাম 100)")

    # STEP 3: QUANTITY + ORDER CREATE
    elif user_step[uid] == "qty":

        if not text.isdigit() or int(text) < 100:
            bot.send_message(uid, "❌ মিনিমাম 100 দিতে হবে")
            return

        qty = int(text)
        sid = temp_order[uid]["sid"]

        # PRICE CALCULATION
        cost = (qty / 1000) * prices[sid]
        cost = round(cost, 2)

        # BALANCE CHECK
        if balance.get(uid, 0) < cost:
            bot.send_message(uid,
                f"❌ পর্যাপ্ত ব্যালেন্স নেই\n\n"
                f"💰 লাগবে: {cost}৳\n"
                f"💼 আপনার ব্যালেন্স: {balance.get(uid,0)}৳"
            )
            user_step[uid] = None
            return

        # BALANCE CUT
        balance[uid] -= cost

        # ORDER ID
        order_id = len(orders) + 1

        orders[order_id] = {
            "user": uid,
            "service": temp_order[uid]["service"],
            "link": temp_order[uid]["link"],
            "quantity": qty,
            "price": cost,
            "status": "Processing"
        }

        # USER MSG
        bot.send_message(uid,
            f"✅ অর্ডার সফল!\n\n"
            f"🆔 Order ID: {order_id}\n"
            f"📦 Service: {temp_order[uid]['service']}\n"
            f"🔢 Quantity: {qty}\n"
            f"💰 Cost: {cost}৳\n"
            f"💼 Remaining Balance: {balance[uid]}৳"
        )

        # ADMIN MSG
        bot.send_message(ADMIN_ID,
            f"📥 নতুন অর্ডার\n\n"
            f"🆔 ID: {order_id}\n"
            f"👤 User: {uid}\n"
            f"📦 Service: {temp_order[uid]['service']}\n"
            f"🔗 Link: {temp_order[uid]['link']}\n"
            f"🔢 Quantity: {qty}\n"
            f"💰 Price: {cost}৳"
        )

        user_step[uid] = None

#================= ORDER STATUS =================
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

# ================= SUPPORT =================
@bot.message_handler(func=lambda m: m.text == "🆘 সাপোর্ট")
def support(message):
    bot.send_message(message.chat.id, "📞 যোগাযোগ: @BOOM_BHAI")

# ================= RUN =================
print("🔥 EL SMM ZONE Bot চালু হয়েছে...")
bot.infinity_polling(skip_pending=True)
