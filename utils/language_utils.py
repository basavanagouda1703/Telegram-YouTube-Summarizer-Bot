def detect_language(user_text):
    language = "English"

    if "kannada" in user_text.lower() or "kannadadalli" in user_text.lower():
        language = "Kannada"

    return language