# Development Guide

## Quick Start

This guide covers how to use the development tools and workflows in the Glove and Mitten project.

## Prerequisites

- **Google Cloud CLI** with Text-to-Speech API enabled
- **Python 3.12+** with required packages
- **ffmpe### Planned Features

1. **Interactive Audio Player**: Pause, play, rewind, fast-forward controls
2. **Editor Integration**: Auto-open character files during TTS playback
3. **Batch Processing**: Multiple character reading sessions
4. **Voice Customization**: Per-character voice selection
5. **Enhanced Chat Analysis**: Deeper insights from conversation patterns

### Recently Implemented

1. ✅ **Chat Automation**: VS Code session tracking with daily summaries
2. ✅ **Development Tracking**: Historical context preservation across sessions
3. ✅ **Timezone Correction**: Accurate local time display in summaries
4. ✅ **Git Integration**: Automated commit-local workflow with Google Drive sync audio processing
- **mpg123** for audio playback
- **make** for workflow automation
- **VS Code** for chat automation integration
- **rclone** for Google Drive synchronization

## Text-to-Speech (TTS) System

### Setup

1. **Google Cloud Configuration**
   ```bash
   # Set up Google Cloud project
   gcloud config set project glove-mitten-tts-1753063317
   
   # Authenticate (if not already done)
   gcloud auth application-default login
   ```

2. **Python Dependencies**
   ```bash
   pip install google-cloud-texttospeech
   ```

### Usage

#### Basic TTS Commands

```bash
# Read a character profile with TTS
make read-profile CHAR=glove

# Test mode (shorter audio for quick testing)
make read-profile CHAR=glove TEST=1

# List available characters
make read-profile
```

#### Available Characters

The system automatically discovers characters from `content/characters/`:
- **Main characters**: `glove`, `mitten`, `fingers-and-hand`
- **School-daze characters**: `principal-watch`, `instructor-beaker`
- **Mis-adventures characters**: (add as created)

#### Voice Configuration

TTS settings are configured in `dev/config/tts-config.json`:

```json
{
  "voice": {
    "language_code": "en-US",
    "name": "en-US-Neural2-J",
    "ssml_gender": "NEUTRAL"
  },
  "audio_config": {
    "audio_encoding": "MP3",
    "speaking_rate": 0.9,
    "pitch": 0.0
  }
}
```

**Available Neural2 Voices:**
- `en-US-Neural2-A` through `en-US-Neural2-J`
- Each has different characteristics (male/female/neutral)

### Audio Cache Management

- **Location**: `dev/cache/audio-cache/`
- **Format**: `tts-{character}-{timestamp}.mp3`
- **Exclusions**: Audio cache is excluded from Git and Google Drive sync
- **Cleanup**: Cache files can be safely deleted to regenerate audio

### How TTS Works

1. **Text Processing**: Character markdown files are processed to extract text content
2. **Chunking**: Long text is split into 5000-byte chunks (Google Cloud TTS limit)
3. **Synthesis**: Each chunk is converted to audio using Google Cloud TTS
4. **Combining**: Multiple chunks are combined using ffmpeg
5. **Playback**: Final audio is played using mpg123

## Chat Automation System

### Overview

The project includes automated VS Code chat session tracking that captures development conversations and generates daily summaries. This system provides context preservation across multi-day development sessions.

### How It Works

1. **VS Code Integration**: Monitors VS Code chat sessions stored in workspace storage
2. **Daily Processing**: Automatically runs at 11:50 PM to analyze the day's conversations
3. **Smart Filtering**: Only includes conversations from the target date using individual message timestamps
4. **Summary Generation**: Creates structured markdown summaries with insights and context
5. **Historical Tracking**: Maintains complete development history in `dev/logs/conversation-summaries/`

### Features

- **Automatic Operation**: No manual intervention required
- **Accurate Dating**: Uses individual message timestamps, not session metadata
- **Local Timezone**: Displays times in local timezone (EDT) instead of UTC
- **Context Preservation**: Tracks decisions, problems solved, and next steps
- **Git Integration**: All summaries are version controlled and synced to Google Drive

### Usage

The system runs automatically, but you can:

```bash
# Check system status
./dev/scripts/setup-daily-summaries.sh status

# Test summary generation
./dev/scripts/setup-daily-summaries.sh test

# View conversation summaries
ls dev/logs/conversation-summaries/
```

### Benefits

- **Never lose context** between development sessions
- **Track technical decisions** and problem-solving approaches
- **Document project evolution** over time
- **Enable easy handoffs** between team members or AI assistants

## Makefile Commands

### Core Workflows

```bash
# TTS System
make read-profile CHAR=character_name    # Generate and play character audio
make read-profile CHAR=character TEST=1  # Quick test mode
make list-characters                     # List available character profiles
make list-voices                        # List available TTS voices

# Project Management
make commit-local                        # Git commit + GitHub + Google Drive sync
make sync                               # Alias for commit-local
make help                               # Show all available commands
make clean                             # Clean up temporary files
make status                            # Show project status

# Episode Production
make process-episode EPISODE=name      # Process episode for production

# Development Tracking (automated)
# Chat sessions are automatically captured and summarized daily
# See dev/logs/conversation-summaries/ for session history
```

### Makefile Structure

The Makefile provides a simple interface to complex workflows:
- **Path Management**: All script paths use `dev/scripts/`
- **Parameter Validation**: Automatic checking of required parameters
- **Help System**: Built-in help and parameter discovery

## Development Tools Structure

```
dev/
├── scripts/                    # Automation scripts
│   ├── read-profile.py        # TTS character reading script
│   ├── parse-chat-sessions.py # VS Code chat session extraction
│   ├── daily-session-summary.sh # Automated development tracking
│   └── setup-daily-summaries.sh # Session automation setup
├── config/                    # Configuration files
│   └── tts-config.json       # TTS voice and audio settings
├── docs/                      # Development documentation
│   ├── project-structure.md   # Content organization guide
│   └── development-guide.md   # This file
├── logs/                      # Development tracking
│   └── conversation-summaries/ # VS Code chat session summaries
│       ├── README.md          # Chat automation documentation
│       └── YYYY-MM-DD-session.md # Daily session summaries
└── cache/                     # Temporary files (not synced)
    └── audio-cache/           # TTS generated audio files
```

## Configuration Management

### TTS Configuration (`dev/config/tts-config.json`)

- **Voice Settings**: Language, voice name, gender
- **Audio Settings**: Encoding, speaking rate, pitch
- **Customization**: Modify settings and regenerate audio to test changes

### Environment Configuration

- **Google Cloud**: Uses application default credentials
- **Python Environment**: Uses system Python (consider virtual env for production)
- **Audio Tools**: Requires ffmpeg and mpg123 in PATH

## Workflows

### Character Development Workflow

1. **Create Character**: Add markdown file to `content/characters/main/` or `content/characters/sagas/`
2. **Test Audio**: `make read-profile CHAR=character_name TEST=1`
3. **Refine Content**: Edit character file based on audio review
4. **Generate Final**: `make read-profile CHAR=character_name`

### Development Workflow

1. **Make Changes**: Edit scripts, configuration, or content
2. **Test Locally**: Use `TEST=1` mode for quick validation
3. **Validate Full**: Run complete workflows to ensure everything works
4. **Document**: Update relevant documentation files

## Troubleshooting

### Common Issues

**Google Cloud Authentication**
```bash
# Re-authenticate if needed
gcloud auth application-default login

# Verify project setting
gcloud config get-value project
```

**Audio Playback Issues**
- Ensure `mpg123` is installed: `sudo apt-get install mpg123`
- Check audio output device configuration
- Verify MP3 files are generated in cache directory

**TTS Errors**
- Check Google Cloud billing is enabled
- Verify Text-to-Speech API is enabled
- Check internet connectivity
- Review cache directory permissions

**File Path Issues**
- All paths are relative to project root
- Use absolute paths in scripts for reliability
- Check that reorganized folder structure matches expectations

### Debug Mode

Add debug output to scripts:
```python
# In read-profile.py, add verbose output
print(f"Processing character: {character_name}")
print(f"Audio cache location: {cache_dir}")
```

## Future Enhancements

### Planned Features

1. **Interactive Audio Player**: Pause, play, rewind, fast-forward controls
2. **Editor Integration**: Auto-open character files during TTS playback
3. **Episode Processing**: PowerPoint to video automation
4. **Batch Processing**: Multiple character reading sessions
5. **Voice Customization**: Per-character voice selection

### Extension Points

- **New Scripts**: Add to `dev/scripts/` and integrate with Makefile
- **Configuration**: Extend `dev/config/` for new tool settings
- **Documentation**: Add new guides to `dev/docs/`
- **Caching**: Extend `dev/cache/` for other temporary files
- **Chat Analysis**: Extend `dev/scripts/parse-chat-sessions.py` for deeper insights

## Best Practices

### Development

- **Test Early**: Use `TEST=1` mode for quick iterations
- **Clean Regularly**: Clear cache when testing configuration changes
- **Document Changes**: Update this guide when adding new features
- **Validate Paths**: Double-check file paths after reorganization

### Content Creation

- **Character Consistency**: Follow series-bible.md guidelines
- **Audio Review**: Always listen to generated audio before finalizing
- **Version Control**: Commit content changes separately from tool changes
- **Backup Strategy**: Ensure important audio is backed up before cache cleanup

## Support

For issues or questions:
1. Check this development guide
2. Review `project-structure.md` for content organization
3. Check Makefile help: `make help`
4. Review script source code in `dev/scripts/`
