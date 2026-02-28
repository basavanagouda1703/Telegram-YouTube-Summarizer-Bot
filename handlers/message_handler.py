from telegram import Update
from telegram.ext import ContextTypes
import time

from utils.youtube_utils import extract_video_id, fetch_video_title
from utils.language_utils import detect_language
from services.transcript_service import fetch_transcript
from services.llm_service import generate_summary, answer_question, generate_deepdive


# ============================================================
#    Main Message Handler
# ============================================================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message or not update.message.text:
        return

    user_text = update.message.text
    language = detect_language(user_text)

    context.user_data["language"] = language
    context.user_data["last_used"] = time.time()

    # ===============================
    # If YouTube link
    # ===============================
    if "youtube.com" in user_text or "youtu.be" in user_text:

        video_id = extract_video_id(user_text)

        if not video_id:
            await update.message.reply_text("❌ Invalid YouTube link.")
            return

        try:
            full_text, timestamps = fetch_transcript(video_id)
            title = fetch_video_title(video_id)

            context.user_data["transcript"] = full_text
            context.user_data["timestamps"] = timestamps
            context.user_data["title"] = title

            await update.message.reply_text("✅ Transcript loaded! Generating summary...")

            summary = generate_summary(full_text[:3000], language)
            timestamp_text = "\n".join(timestamps[:5])

            final_response = f"""
🎥 {title}

{summary}

⏱ Important Timestamps:
{timestamp_text}
"""

            await update.message.reply_text(final_response, parse_mode="Markdown")

        except Exception as e:
            print("Transcript error:", e)
            await update.message.reply_text("❌ Transcript not available.")

    # ===============================
    # If user asks question
    # ===============================
    else:

        if "transcript" not in context.user_data:
            await update.message.reply_text("📌 Please send a YouTube link first.")
            return

        transcript_text = context.user_data["transcript"]
        language = context.user_data.get("language", "English")

        answer = answer_question(transcript_text, user_text, language)
        await update.message.reply_text(answer)


# ============================================================
# 📌 /summary
# ============================================================
async def handle_summary_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if "transcript" not in context.user_data:
        await update.message.reply_text("📌 Please send a YouTube link first.")
        return

    transcript_text = context.user_data["transcript"]
    language = context.user_data.get("language", "English")
    title = context.user_data.get("title", "")
    timestamps = context.user_data.get("timestamps", [])

    summary = generate_summary(transcript_text[:3000], language)
    timestamp_text = "\n".join(timestamps[:5])

    final_response = f"""
🎥 {title}

{summary}

⏱ Important Timestamps:
{timestamp_text}
"""

    await update.message.reply_text(final_response, parse_mode="Markdown")


# ============================================================
# 📘 /deepdive
# ============================================================
async def handle_deepdive_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if "transcript" not in context.user_data:
        await update.message.reply_text("📌 Please send a YouTube link first.")
        return

    transcript_text = context.user_data["transcript"]
    language = context.user_data.get("language", "English")

    response = generate_deepdive(transcript_text, language)
    await update.message.reply_text(response)