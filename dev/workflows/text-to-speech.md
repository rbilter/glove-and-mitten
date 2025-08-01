# Text-to-Speech Workflow

## Overview
Provides high-quality text-to-speech reading of charac### Usage Examples

### Character Profile Reading
```bash
# Natural language commands
"Read Glove profile"
"Use TTS for Mitten" 
"read-profile Principal Watch"
```and other markdown content using Google Cloud Text-to-Speech.

## Usage
**Natural Language Commands:**

**Assistant Integration:**
- "Read me the [character name] profile"
- "Read the Glove character profile"
- "Run TTS on Mitten character"
- "Use text-to-speech for Principal Watch"

## What the TTS Workflow Does:
1. ✅ **Cleans markdown** - Removes formatting for better speech
2. ✅ **Calls Google Cloud TTS** - High-quality neural voices
3. ✅ **Plays audio** - Streams or saves audio output
4. ✅ **Manages credentials** - Secure API key handling
5. ✅ **Caches audio** - Saves generated audio files for reuse

## Setup Requirements

### One-Time Setup
1. **Install Google Cloud CLI**
   ```bash
   # Install gcloud (if not already installed)
   curl https://sdk.cloud.google.com | bash
   exec -l $SHELL  # Restart shell
   ```

2. **Install Python Dependencies**
   ```bash
   pip install google-cloud-texttospeech markdown
   ```

3. **Setup Google Cloud Project & Authentication**
   ```bash
   # Login to Google Cloud
   gcloud auth login
   
   # Create or select project
   gcloud projects create glove-mitten-tts --name="Glove and Mitten TTS"
   gcloud config set project glove-mitten-tts
   
   # Enable Text-to-Speech API
   gcloud services enable texttospeech.googleapis.com
   
   # Create service account and key
   gcloud iam service-accounts create tts-reader --display-name="TTS Reader"
   gcloud projects add-iam-policy-binding glove-mitten-tts \
     --member="serviceAccount:tts-reader@glove-mitten-tts.iam.gserviceaccount.com" \
     --role="roles/cloudtts.user"
   gcloud iam service-accounts keys create ~/.gcp-tts-key.json \
     --iam-account=tts-reader@glove-mitten-tts.iam.gserviceaccount.com
   
   # Set environment variable
   export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.gcp-tts-key.json"
   echo 'export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.gcp-tts-key.json"' >> ~/.bashrc
   ```

## Workflow Scripts

### Main TTS Script: `scripts/read-profile.py`
- Converts markdown to clean text
- Calls Google Cloud TTS API
- Plays audio or saves to file
- Caches results for performance

### Makefile Integration
- `make read-profile CHAR=glove`
- `make read-profile CHAR=mitten TEST=1`
- `make read-profile` (shows available characters)

## Voice Options

### Available Voices (US English):
- **en-US-Neural2-A** - Female, conversational
- **en-US-Neural2-C** - Female, news anchor style  
- **en-US-Neural2-D** - Male, warm and friendly
- **en-US-Neural2-F** - Female, young and bright
- **en-US-Neural2-G** - Female, conversational
- **en-US-Neural2-H** - Female, confident
- **en-US-Neural2-I** - Male, young and friendly
- **en-US-Neural2-J** - Male, casual and warm

### Configuration
Edit `scripts/tts-config.json` to customize:
- Voice selection
- Speaking rate (0.25x to 4.0x)
- Pitch (-20.0 to +20.0 semitones)
- Audio format (MP3, WAV, OGG)

## Usage Examples

### Character Profile Reading
```bash
# Read specific character
make read-profile CHAR=glove

# Test mode (shorter content)
make read-profile CHAR=mitten TEST=1

# List available characters
make read-profile
```

### Assistant Commands
- **"Read me the Glove profile"** → Reads Glove character profile
- **"Read Principal Watch profile"** → Reads Principal Watch character
- **"Use TTS for Mitten"** → Reads Mitten character profile

## File Structure
```
dev/scripts/
├── read-profile.py             # Main TTS script
├── parse-chat-sessions.py      # Chat automation
├── daily-session-summary.sh    # Session tracking
└── setup-daily-summaries.sh    # Automation setup

dev/config/
└── tts-config.json            # Voice and audio settings

dev/cache/
└── audio-cache/               # Generated audio files
    ├── tts-glove-*.mp3
    ├── tts-mitten-*.mp3
    └── ...
```

## Cost Management
- **Free tier**: 1 million characters/month
- **Current usage**: ~60k characters for all profiles
- **Estimated cost**: $0/month (well under free tier)
- **Monitoring**: Script tracks character usage

## Troubleshooting

### Common Issues
1. **"Authentication error"** → Check GOOGLE_APPLICATION_CREDENTIALS
2. **"API not enabled"** → Run `gcloud services enable texttospeech.googleapis.com`
3. **"No audio output"** → Check audio system and volume
4. **"Rate limit exceeded"** → Wait or check API quotas

### Debug Commands
```bash
# Test authentication
gcloud auth list

# Test API access
python3 -c "from google.cloud import texttospeech; print('TTS API available')"

# Check audio system
aplay /usr/share/sounds/alsa/Front_Left.wav
```

## Security Notes
- **Credentials**: Store securely, never commit to git
- **API Keys**: Rotate periodically for security
- **Usage Monitoring**: Track to avoid unexpected charges
- **Network**: Works offline with cached audio files

---

*This workflow provides professional-quality text-to-speech for character profile review and content development while staying within Google Cloud's free tier limits.*
