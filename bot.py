import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("BOT_TOKEN", "YOUR_TOKEN_HERE")
MANAGER_USERNAME = "@Vova_Melnyk_1"

# ── Тексти ──────────────────────────────────────────────────────────────────

TEXT_MAIN = "Що Вас цікавить?"

TEXT_SHELL = (
    "Shell Card — Все в 1 картці:\n\n"
    "✅ Заправка пальним\n"
    "✅ Дорожні збори та сервіси\n"
    "✅ Повернення ПДВ\n"
    "✅ Безпека та онлайн-послуги\n"
    "✅ Замовлення Мультибоксу\n"
    "✅ Контроль витрат\n\n"
    "Оберіть дію, яку бажаєте виконати."
)

TEXT_SHELL_PIN = (
    "❕ Економія часу\n\n"
    "Ваш PIN-код (e-PIN) доступний в особистому кабінеті Shell Fleet Hub "
    "одразу після випуску картки — без очікування та додаткових листів!\n\n"
    "🔍 Обрати дію"
)

TEXT_SHELL_BLOCK = (
    "Якщо потрібна допомога в блокуванні зателефонуйте\n\n"
    "📞 +38 050-509-0-509\n\n"
    "Дякуємо!\n"
    "🔎 Обрати дію"
)

TEXT_SHELL_ORDER = (
    "Бажаєте замовити картку Shell?\n\n"
    "📧 Надішліть лист на office@tsg-euroshell.com.ua\n\n"
    "Дякуємо!\n"
    "🔎 Обрати дію"
)

TEXT_COMING_SOON = "🔧 Цей розділ незабаром буде доступний. Дякуємо за терпіння!"

# ── Клавіатури ───────────────────────────────────────────────────────────────

def kb_main():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 Картка Shell", callback_data="shell")],
        [InlineKeyboardButton("📦 Мультибокс T4E", callback_data="multibox")],
        [InlineKeyboardButton("🖥 Онлайн кабінет", callback_data="cabinet")],
        [InlineKeyboardButton("🛣 Оплата доріг", callback_data="roads")],
        [InlineKeyboardButton("📄 Документи", callback_data="docs")],
        [InlineKeyboardButton("🧾 ПДВ (VAT)", callback_data="vat")],
        [InlineKeyboardButton("📰 Новини", callback_data="news")],
        [InlineKeyboardButton("📞 Контакти", callback_data="contacts")],
    ])

def kb_shell():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔑 Забули пін", callback_data="shell_pin")],
        [InlineKeyboardButton("🚫 Заблокувати", callback_data="shell_block")],
        [InlineKeyboardButton("🛒 Замовити", callback_data="shell_order")],
        [InlineKeyboardButton("💬 Чат з менеджером", url=f"https://t.me/{MANAGER_USERNAME.lstrip('@')}")],
        [InlineKeyboardButton("🏠 До меню", callback_data="main")],
    ])

def kb_back_shell():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("◀️ Назад", callback_data="shell"),
         InlineKeyboardButton("🏠 До меню", callback_data="main")],
    ])

def kb_coming_soon():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 До меню", callback_data="main")],
    ])

# ── Хендлери ─────────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(TEXT_MAIN, reply_markup=kb_main())

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # Головне меню
    if data == "main":
        await query.edit_message_text(TEXT_MAIN, reply_markup=kb_main())

    # Shell
    elif data == "shell":
        await query.edit_message_text(TEXT_SHELL, reply_markup=kb_shell())
    elif data == "shell_pin":
        await query.edit_message_text(TEXT_SHELL_PIN, reply_markup=kb_back_shell())
    elif data == "shell_block":
        await query.edit_message_text(TEXT_SHELL_BLOCK, reply_markup=kb_back_shell())
    elif data == "shell_order":
        await query.edit_message_text(TEXT_SHELL_ORDER, reply_markup=kb_back_shell())

    # Інші розділи — заглушки (заповнимо пізніше)
    elif data in ("multibox", "cabinet", "roads", "docs", "vat", "news", "contacts"):
        await query.edit_message_text(TEXT_COMING_SOON, reply_markup=kb_coming_soon())

# ── Запуск ────────────────────────────────────────────────────────────────────

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    logger.info("Бот запущено")
    app.run_polling()

if __name__ == "__main__":
    main()
