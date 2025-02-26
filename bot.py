import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
import yt_dlp

# Video yuklab olish funksiyasi
async def download_video(link):
    output_file = "video.mp4"
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_file,
        'quiet': True,
        'max_filesize': 500 * 1024 * 1024,  # Maksimal hajm: 500 MB
    }
    try:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).download([link]))
        return output_file if os.path.exists(output_file) else None
    except yt_dlp.utils.DownloadError:
        return None
    except Exception as e:
        print(f"Xatolik: {e}")
        return None

# /start komandasiga javob
async def start(update: Update, context: CallbackContext):
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"Assalomu alaykum, {user_name}! Instagram yoki YouTube havolasini yuboring."
    )

# Inline tugma yaratish
def create_channel_button():
    keyboard = [
        [InlineKeyboardButton("Bizning kanal", url='https://t.me/simplyweb_uzb')]
    ]
    return InlineKeyboardMarkup(keyboard)

# Foydalanuvchi yuborgan havolani qayta ishlash
async def handle_message(update: Update, context: CallbackContext):
    link = update.message.text.strip()
    if "instagram.com" in link or "youtube.com" in link or "youtu.be" in link:
        await update.message.reply_text("Video yuklanmoqda. Iltimos, kuting...")

        # Video yuklash
        video_file = await download_video(link)
        if video_file and os.path.exists(video_file):
            try:
                # Yuklangan videoni yuborish
                with open(video_file, 'rb') as video:
                    await context.bot.send_video(chat_id=update.effective_chat.id, video=video, reply_markup=create_channel_button())
                await update.message.reply_text("✅ Video muvaffaqiyatli yuborildi!")
            except Exception as e:
                await update.message.reply_text(f"⚠️ Video yuborishda xatolik yuz berdi: {e}")
            finally:
                # Faylni tizimdan o'chirish
                os.remove(video_file)
        else:
            await update.message.reply_text("⚠️ Video yuklab bo'lmadi yoki havola noto'g'ri.")
    else:
        await update.message.reply_text("❌ Iltimos, Instagram yoki YouTube havolasini yuboring.")

# Asosiy bot funksiyasi
def main():
    # Tokeningizni bu yerga kiriting
    TOKEN = "TOKENNI_BU_YERGA_KIRITING"
    app = ApplicationBuilder().token(TOKEN).build()

    # Komandalar va xabarlarni boshqarish
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Botni ishga tushirish
    print("🤖 Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
