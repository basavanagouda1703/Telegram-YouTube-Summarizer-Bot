from youtube_transcript_api import YouTubeTranscriptApi

video_cache = {}


def format_timestamp(seconds):
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"


def fetch_transcript(video_id):

    # 🔹 Check cache first
    if video_id in video_cache:
        return video_cache[video_id]

    ytt = YouTubeTranscriptApi()
    transcript = ytt.fetch(video_id)

    full_text = " ".join([t.text for t in transcript])

    timestamps = []
    for t in transcript[::50]:
        seconds = int(t.start)
        time_label = format_timestamp(seconds)

        timestamps.append(
            f"[{time_label}](https://www.youtube.com/watch?v={video_id}&t={seconds}s)"
        )

    video_cache[video_id] = (full_text, timestamps)

    return full_text, timestamps