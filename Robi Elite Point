import telebot
from telebot.types import ReplyKeyboardMarkup
import sqlite3

TOKEN = "8571658044:AAEIR_3ZgS5YxdEqZ_TJCqhPEx8Qa2bKhB8"
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 7268416193

# ================= DATABASE =================
conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    balance INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS sell_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    point INTEGER,
    amount INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS withdraw_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount INTEGER,
    number TEXT
)
""")

conn.commit()

# ================= FUNCTIONS =================
def get_balance(uid):
    cursor.execute("SELECT balance FROM users WHERE user_id=?", (uid,))
    data = cursor.fetchone()
    return data[0] if data else 0

def add_balance(uid, amt):
    bal = get_balance(uid)
    cursor.execute("INSERT OR REPLACE INTO users VALUES (?, ?)", (uid, bal + amt))
    conn.commit()

def minus_balance(uid, amt):
    bal = get_balance(uid)
    cursor.execute("UPDATE users SET balance=? WHERE user_id=?", (bal - amt, uid))
    conn.commit()

# ================= MENU =================
def menu():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.add("💰 Sell", "💳 Withdraw")
    m.add("📊 Balance", "📞 Support")
    return m

# ================= START =================
@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id,
"""🏡 WELCOME TO ROBI ELITE BOT

💰 1K Point = 150৳
📉 Min Sell: 300 Point
💳 Withdraw: 100-5000৳

👇 Menu select করুন""",
reply_markup=menu())

# ================= SELL =================
user_sell = {}

@bot.message_handler(func=lambda m: m.text == "💰 Sell")
def sell(m):
    user_sell[m.chat.id] = "point"
    bot.send_message(m.chat.id, "🔢 কত Point Sell করবেন?")

@bot.message_handler(func=lambda m: m.chat.id in user_sell)
def sell_process(m):
    uid = m.chat.id

    if user_sell[uid] == "point":
        try:
            point = int(m.text)

            if point < 300:
                bot.send_message(uid, "❌ Minimum 300 point")
                return

            amount = int((point / 1000) * 150)

            cursor.execute(
                "INSERT INTO sell_history (user_id, point, amount) VALUES (?, ?, ?)",
                (uid, point, amount)
            )
            conn.commit()

            bot.send_message(uid,
f"""📊 SELL INFO

Point: {point}
Amount: {amount}৳

📞 Send to:
01895288899

📸 Screenshot দিন""")

        except:
            bot.send_message(uid, "❌ শুধু সংখ্যা দিন")

# ================= SCREENSHOT =================
@bot.message_handler(content_types=['photo'])
def photo(m):
    bot.send_photo(ADMIN_ID, m.photo[-1].file_id,
caption=f"""📸 SELL REQUEST

User: {m.chat.id}

Approve:
👉 /add {m.chat.id} amount""")

# ================= BALANCE =================
@bot.message_handler(func=lambda m: m.text == "📊 Balance")
def bal(m):
    bot.send_message(m.chat.id, f"💰 Balance: {get_balance(m.chat.id)}৳")

# ================= SUPPORT =================
@bot.message_handler(func=lambda m: m.text == "📞 Support")
def sup(m):
    bot.send_message(m.chat.id, "@BOOM_BHAI")

# ================= WITHDRAW =================
user_wd = {}

@bot.message_handler(func=lambda m: m.text == "💳 Withdraw")
def wd(m):
    user_wd[m.chat.id] = "amount"
    bot.send_message(m.chat.id, "💰 কত টাকা তুলবেন?")

@bot.message_handler(func=lambda m: m.chat.id in user_wd)
def wd_process(m):
    uid = m.chat.id

    if user_wd[uid] == "amount":
        amount = int(m.text)

        if amount < 100 or amount > 5000:
            bot.send_message(uid, "❌ 100-5000")
            return

        if amount > get_balance(uid):
            bot.send_message(uid, "❌ Balance নাই")
            return

        user_wd[uid] = {"amount": amount}
        bot.send_message(uid, "📱 নাম + নাম্বার দিন")

    else:
        amount = user_wd[uid]["amount"]

        minus_balance(uid, amount)

        cursor.execute(
            "INSERT INTO withdraw_history (user_id, amount, number) VALUES (?, ?, ?)",
            (uid, amount, m.text)
        )
        conn.commit()

        bot.send_message(uid, "✅ Request sent")
        bot.send_message(ADMIN_ID, f"Withdraw: {uid} → {amount}৳ → {m.text}")

        del user_wd[uid]

# ================= ADMIN ADD =================
@bot.message_handler(commands=['add'])
def add(m):
    if m.chat.id != ADMIN_ID:
        return

    try:
        _, uid, amt = m.text.split()
        uid = int(uid)
        amt = int(amt)

        add_balance(uid, amt)

        bot.send_message(uid, f"✅ {amt}৳ Added")
        bot.send_message(m.chat.id, "✔ Done")

    except:
        bot.send_message(m.chat.id, "❌ ভুল format")

# ================= RUN =================
print("🔥 BOT RUNNING...")
bot.infinity_polling()
