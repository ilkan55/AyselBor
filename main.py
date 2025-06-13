from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import *
from aiogram.enums import ChatMemberStatus
from aiogram.filters import CommandStart, Command, ChatMemberUpdatedFilter
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio
import datetime
import logging

API_TOKEN = "BOT_TOKENINIZI_YAZIN"
OWNER_USERNAME = "@Qocadi"
LOG_CHANNEL_ID = -1001234567890  # Log kanal ID

bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher()
router = Router()

# START mesajı
@router.message(CommandStart())
async def start_handler(message: Message):
    user = message.from_user.first_name
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Məni Qrupuna Əlavə Et", url=f"https://t.me/{(await bot.me()).username}?startgroup=true")],
        [InlineKeyboardButton(text="📚 Komandalar", callback_data="commands")],
        [InlineKeyboardButton(text="📤 Support", url=f"https://t.me/{OWNER_USERNAME.strip('@')}")],
        [InlineKeyboardButton(text="🧑‍💻 Sahibim", url=f"https://t.me/{OWNER_USERNAME.strip('@')}")],
        [InlineKeyboardButton(text="ℹ️ Bot haqqında", callback_data="cmd_info")]
    ])
    await message.answer_photo(
        photo="https://telegra.ph/file/your-image.jpg",
        caption=f"""
╔═.✵.═══════════════════╗
║▻ Salam {user} 👏
║▻ Mənim adım Aysel 🙎
║▻ Mən Telegramda Çox funksiyalı 🐾
║▻ Telegram robotuyam 🗣️
║▻ Mənim əmrlərimi görmək üçün 👁️
║▻ 📚Komandalar buttonuna basın
║▻ 🧑‍💻Sahibim {OWNER_USERNAME} 🦅
╚═══════════════════.✵.═╝
        """,
        reply_markup=keyboard
    )
    await bot.send_message(LOG_CHANNEL_ID, f"✅ Start: {user} ({message.from_user.id})")

# KOMANDALAR menyusu
@router.callback_query(F.data == "commands")
async def commands_callback(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📌 /pin", callback_data="cmd_pin"), InlineKeyboardButton(text="❌ /unpin", callback_data="cmd_unpin")],
        [InlineKeyboardButton(text="🧹 /unpinall", callback_data="cmd_unpinall"), InlineKeyboardButton(text="👥 /adminlist", callback_data="cmd_adminlist")],
        [InlineKeyboardButton(text="🧑‍💻 /admin", callback_data="cmd_admin")],
        [InlineKeyboardButton(text="🆔 /id", callback_data="cmd_id"), InlineKeyboardButton(text="👤 /men", callback_data="cmd_men")],
        [InlineKeyboardButton(text="⏰ /time", callback_data="cmd_time"), InlineKeyboardButton(text="💬 /chat", callback_data="cmd_chat")],
        [InlineKeyboardButton(text="🔇 /mute", callback_data="cmd_mute"), InlineKeyboardButton(text="🔊 /unmute", callback_data="cmd_unmute")],
        [InlineKeyboardButton(text="🚫 /ban", callback_data="cmd_ban"), InlineKeyboardButton(text="♻️ /unban", callback_data="cmd_unban")],
        [InlineKeyboardButton(text="🔔 /name on", callback_data="cmd_nameon"), InlineKeyboardButton(text="🔕 /name off", callback_data="cmd_nameoff")],
        [InlineKeyboardButton(text="ℹ️ /info", callback_data="cmd_info")],
        [InlineKeyboardButton(text="🔙 Geri", callback_data="back_start")]
    ])
    await callback.message.edit_caption(
        caption=f"╔═.✵.═══════════════════╗\n║▻ Sənə uyğun olan ✅\n║▻ Button komandasına toxun\n║▻ 🧑‍💻Sahibim {OWNER_USERNAME} 🦅\n╚═══════════════════.✵.═╝",
        reply_markup=keyboard
    )

# CALLBACK əmrlərin açıqlaması
@router.callback_query(F.data.startswith("cmd_"))
async def command_info(callback: CallbackQuery):
    cmd = callback.data[4:]
    info = {
        "pin": "Mesajı pin edər (yalnız qruplarda).",
        "unpin": "Mesajı pindən çıxarar.",
        "unpinall": "Bütün pinləri silər.",
        "adminlist": "Qrup adminlərini göstərər.",
        "admin": "Admin hüquqlarını göstərər.",
        "id": "İstifadəçinin ID nömrəsini göstərər.",
        "men": "İstifadəçi haqqında məlumat verər.",
        "time": "Qrupda saatı göstərər.",
        "chat": "Qrup haqqında məlumat verir.",
        "info": "Bot haqqında məlumat verir.",
        "mute": "İstifadəçini səssiz edir.",
        "unmute": "Səssizliyi açar.",
        "ban": "İstifadəçini banlayar.",
        "unban": "Banı açar.",
        "nameon": "Ad dəyişikliklərini izləməyə başlar.",
        "nameoff": "Ad izləmə deaktiv olur."
    }
    text = info.get(cmd, "Bu əmrlə bağlı məlumat tapılmadı.")
    await callback.message.edit_caption(
        caption=f"╔═══════════════╗\n║▻ 🆕 /{cmd}\n║▻ 🔁 açıqlama: {text}\n╚═══════════════╝",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 Geri", callback_data="commands")]])
    )

# Geri qaytarma
@router.callback_query(F.data == "back_start")
async def back_to_start(callback: CallbackQuery):
    await start_handler(callback.message)

# Əsas funksiyalar (məsələn, /pin)
@router.message(Command("pin"))
async def pin_message(message: Message):
    if not message.chat.type.name.startswith("GROUP"):
        return
    if not message.reply_to_message:
        await message.reply("Zəhmət olmasa hər hansısa bir mesaja cavab verin ✅")
    else:
        await bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
        await message.reply("Mesaj pin edildi.")

# /unpin, /unpinall, /adminlist, /ban, /mute və s. eyni formada əlavə olunacaq...

# NÜMUNƏ: Azərbaycan saatı
@router.message(Command("time"))
async def cmd_time(message: Message):
    az_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=4)))
    await message.reply(f"⏰ Azərbaycan saatı: {az_time.strftime('%H:%M:%S')}")

# Xoş gəldin mesajı
@router.message(Command("welcome"))
async def welcome_handler(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Xoş gəldin Aktif", callback_data="welcome_active")],
        [InlineKeyboardButton(text="❌ Xoş gəldin deaktif", callback_data="welcome_inactive")],
        [InlineKeyboardButton(text="✍️ Xoş gəldin dəyişdir", callback_data="welcome_edit")]
    ])
    await message.answer("Xoş gəldin mesajını seçin:", reply_markup=keyboard)

# Səsli Söhbət mesaja cavab
@router.chat_member(ChatMemberUpdatedFilter())
async def voice_chat_handler(update: ChatMemberUpdated):
    if update.new_chat_member.status == ChatMemberStatus.VOICE_CHAT:
        await bot.send_message(update.chat.id, f"Səsli Söhbət zamanı başladı 🦅")

    elif update.new_chat_member.status == ChatMemberStatus.LEFT:
        await bot.send_message(update.chat.id, f"Səsli Söhbət bağlandı 🥲")

# Səsli Söhbətə dəvət
@router.chat_member(ChatMemberUpdatedFilter())
async def voice_invite_handler(update: ChatMemberUpdated):
    if update.new_chat_member.status == ChatMemberStatus.VOICE_CHAT:
        user = update.new_chat_member.user.first_name
        await bot.send_message(update.chat.id, f"{user} hey sən😊\nSəslidə dəvətin var😍\nSəni gözləyirik 🌛\nHadi qalx səsə")

# Admin siyahısı
@router.message(Command("adminlist"))
async def adminlist(message: Message):
    admins = [admin.user.first_name for admin in await bot.get_chat_administrators(message.chat.id)]
    await message.reply(f"Admin siyahısı: {', '.join(admins)}")

# Start polling
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    dp.include_router(router)
    asyncio.run(dp.start_polling(bot))
