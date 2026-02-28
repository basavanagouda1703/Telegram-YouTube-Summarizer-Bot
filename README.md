# Telegram-YouTube-Summarizer-Bot

# Setup Steps
1. Install Dependencies
->Install required Python packages by using below command :
"pip install python-telegram-bot youtube-transcript-api requests"

2. Install ollama
->Download Ollama from:
https://ollama.com/download
->After installation run the below commands:
"ollama pull llama3"
"ollama serve"

3. Configure Telegram Bot Token
->Create a bot using BotFather in Telegram.
->Add the token inside config.py:
BOT_TOKEN = "TELEGRAM_BOT_TOKEN"

4. Run the Bot
Start the application by running:
python main.py

# Architecture
# 1. Project Structure :

telegram-youtube-bot/
├── main.py                
├── config.py              
├── handlers/               
│   └── message_handler.py
├── services/              
│   ├── transcript_service.py
│   └── llm_service.py
└── utils/                  
    ├── youtube_utils.py
    └── language_utils.py

# 2. Data Flow Overview:

   User -> Telegram Bot -> Message Handler ->Transcript Service -> YouTube Title Fetch -> LLM Service (Ollama) -> Response

# 3. Component Responsibilities:
   
i. main.py
->Initializes Telegram bot
->Registers command and message handlers
->Starts polling

ii. message_handler.py
->Detects user intent
->Differentiates between:
   ->YouTube link
   ->Question
   ->Commands (/summary, /deepdive)

iii. transcript_service.py
->Fetches transcript from YouTube
->Extracts clickable timestamps
->Implements in-memory caching by video_id

iv. llm_service.py
->Sends structured prompts to Ollama
->Handles:
   ->Summary generation
   ->Q&A generation
   ->Deep-dive explanation

v. youtube_utils.py
->Extracts video ID
->Fetches video title

vi. language_utils.py
->Detects if user requested Kannada
->Defaults to English

# Design Trade-offs
# 1. Using Ollama (Local LLM) Instead of OpenAI API
i. Advantages:
->No API cost
->Works offline
->Full control over model
->Privacy-friendly
ii. Trade-off:
->Requires local system resources
->Slower than cloud APIs
->Limited by hardware capability

# 2. Transcript Truncation (First 3000 Characters)
Only a portion of transcript is sent to the model.
i. Advantages:
->Prevents context overflow
->Improves response speed
->Avoids model timeouts
ii. Trade-off:
->Very long videos may lose context from later sections

# 3. In-Memory Caching Instead of Database
Used dictionary cache for transcripts.
i. Advantages:
->Simple implementation
->Faster response
->Assignment scope appropriate
ii. Trade-off:
->Cache resets when bot restarts
->Not persistent

# 4. Language Support via Prompt Engineering
Instead of using a translation API.
i. Advantages:
->Simpler architecture
->No external API
->Faster integration
ii. Trade-off:
->Model output quality depends on LLM capability
