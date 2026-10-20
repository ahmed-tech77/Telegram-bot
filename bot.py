import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import yt_dlp

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = "ضع_التوكن_الخاص_بك_هنا"

def download_video(url: str) -> str:
    output_template = 'downloaded_video.%(ext)s'
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': output_template,
        'merge_output_format': 'mp4',
        'noplaylist': True,
        'quiet': True,
    }
    
    for ext in ['mp4', 'webm', 'mkv', 'mov']:
        filename = f'downloaded_video.{ext}'
        if os.path.exists(filename):
            os.remove(filename)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        if not filename.endswith('.mp4') and os.path.exists('downloaded_video.mp4'):
            return 'downloaded_video.mp4'
        return filename

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    
    if not url.startswith("http"):
        await update.message.reply_text("يرجى إرسال رابط فيديو صالح.")
        return

    msg = await update.message.reply_text("جاري التحميل... ⏳")
    
    try:
        file_path = download_video(url)
        
        with open(file_path, 'rb') as video_file:
            await update.message.reply_video(video=video_file, caption="تم التحميل بنجاح! 🚀")
            
        await msg.delete()
        if os.path.exists(file_path):
            os.remove(file_path)
            
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("عذراً، حدث خطأ أثناء التحميل. تأكد من صحة الرابط.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("البوت يعمل...")
    app.run_polling()
  
