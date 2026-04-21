import os
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("BOT_TOKEN")
MANAGER = "Vova_Melnyk_1"

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

TEXT_PIN = (
    "❕ Економія часу\n\n"
    "Ваш PIN-код (e-PIN) доступний в особистому кабінеті Shell Fleet Hub "
    "одразу після випуску картки — без очікування та додаткових листів!\n\n"
    "🔍 Обрати дію"
)

TEXT_BLOCK = (
    "Якщо потрібна допомога в блокуванні зателефонуйте\n\n"
    "📞 +38 050-509-0-509\n\n"
    "Дякуємо!\n"
    "🔎 Обрати дію"
)

TEXT_ORDER = (
    "Бажаєте замовити картку Shell?\n\n"
    "📧 Надішліть лист на office@tsg-euroshell.com.ua\n\n"
    "Дякуємо!\n"
    "🔎 Обрати дію"
)

TEXT_SOON = "🔧 Цей розділ незабаром буде доступний. Дякуємо за терпіння!"


def main_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 Картка Shell", callback_data="shell")],
        [InlineKeyboardButton("📦 Мультибокс T4E", callback_data="soon")],
        [InlineKeyboardButton("🖥 Онлайн кабінет", callback_data="soon")],
        [InlineKeyboardButton("🛣 Оплата доріг", callback_data="soon")],
        [InlineKeyboardButton("📄 Документи", callback_data="soon")],
        [InlineKeyboardButton("🧾 ПДВ (VAT)", callback_data="soon")],
        [InlineKeyboardButton("📰 Новини", callback_data="soon")],
        [InlineKeyboardButton("📞 Контакти", callback_data="soon")],
    ])


def shell_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔑 Забули пін", callback_data="pin")],
        [InlineKeyboardButton("🚫 Заблокувати", callback_data="block")],
        [InlineKeyboardButton("🛒 Замовити", callback_data="order")],
        [InlineKeyboardButton("💬 Чат з менеджером", url=f"https://t.me/{MANAGER}")],
        [InlineKeyboardButton("🏠 До меню", callback_data="main")],
    ])


def back_kb():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("◀️ Назад", callback_data="shell"),
            InlineKeyboardButton("🏠 До меню", callback_data="main"),
        ]
    ])


def soon_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 До меню", callback_data="main")]
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(TEXT_MAIN, reply_markup=main_kb())


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    d = q.data

    if d == "main":
        await q.edit_message_text(TEXT_MAIN, reply_markup=main_kb())
    elif d == "shell":
        await q.edit_message_text(TEXT_SHELL, reply_markup=shell_kb())
    elif d == "pin":
        await q.edit_message_text(TEXT_PIN, reply_markup=back_kb())
    elif d == "block":
        await q.edit_message_text(TEXT_BLOCK, reply_markup=back_kb())
    elif d == "order":
        await q.edit_message_text(TEXT_ORDER, reply_markup=back_kb())
    elif d == "soon":
        await q.edit_message_text(TEXT_SOON, reply_markup=soon_kb())


async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle))
    print("Бот запущено")
    async with app:
        await app.start()
        await app.updater.start_polling(drop_pending_updates=True)
        await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
