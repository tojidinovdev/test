import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import yt_dlp

# Instagramdan video yuklab olish uchun funksiya
def download_instagram_video(link):
    output_file = "video.mp4"
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_file,
        'max_filesize': 50 * 1024 * 1024,  # Maksimal hajm: 50 MB
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        return output_file
    except yt_dlp.utils.DownloadError as e:
        print(f"Yuklash xatosi: {e}")
        return None
    except Exception as e:
        print(f"Xatolik: {e}")
        return None

# /start komandasiga javob
async def start(update: Update, context):
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"Assalomu alaykum, {user_name}! Instagram video havolasini yuboring."
    )

# Instagram video havolasini qayta ishlash va yuborish
async def handle_message(update: Update, context):
    link = update.message.text
    if "instagram.com" in link:
        await update.message.reply_text("Videoni yuklab olayapman. Bir oz kuting...")
        
        video_file = download_instagram_video(link)
        if video_file:
            try:
                with open(video_file, 'rb') as video:
                    await context.bot.send_video(chat_id=update.effective_chat.id, video=video)
                await update.message.reply_text("Video muvaffaqiyatli yuborildi!")
            except Exception as e:
                await update.message.reply_text(f"Video yuborishda xatolik yuz berdi: {e}")
            finally:
                # Faylni tizimdan o'chirish
                if os.path.exists(video_file):
                    os.remove(video_file)
        else:
            await update.message.reply_text("Videoni yuklab bo'lmadi yoki havola noto'g'ri.")
    else:
        await update.message.reply_text("Iltimos, to'g'ri Instagram video havolasini yuboring.")

# Asosiy bot funksiyasi
def main():
    # Tokeningizni bu yerga kiriting
    TOKEN = "7916787690:AAHujBAn3eZn8iPahWmBZzbvUmBshg3n1dg"
    app = Application.builder().token(TOKEN).build()

    # Komandalar
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Botni ishga tushirish
    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
