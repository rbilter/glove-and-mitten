# Project Structure Documentation

## Current Status: **50 directories, 97 files**

Complete project organization with comprehensive asset library, production workflows, and automated development tracking.

## Implemented Structure

```
glove-and-mitten/
├── content/                           # 🎭 CREATIVE CONTENT
│   ├── assets/
│   │   ├── images/
│   │   │   ├── background/
│   │   │   │   ├── school-buildings/
│   │   │   │   ├── classroom/
│   │   │   │   ├── principal-office/
│   │   │   │   ├── playground/
│   │   │   │   ├── characters/
│   │   │   │   ├── nature/
│   │   │   │   └── props/
│   │   │   ├── glove/
│   │   │   ├── gloveandmitten/
│   │   │   └── mitten/
│   │   ├── audio/
│   │   └── templates/
│   ├── characters/
│   │   ├── main/
│   │   └── sagas/
│   │       ├── school-daze/
│   │       └── mis-adventures/
│   └── stories/
│       ├── ideas/
│       │   ├── mis-adventures/
│       │   └── school-daze/
│       └── sagas/
│           ├── mis-adventures/
│           │   └── stories/
│           └── school-daze/
│               └── stories/
│                   └── lights/
│                       └── tuff-daze/
├── production/                        # 🎬 FINAL DELIVERABLES
│   ├── completed/
│   │   ├── metadata/
│   │   │   ├── 01-lights-tuff-daze/
│   │   │   └── templates/
│   │   └── videos/
│   ├── in-progress/
│   └── README.md
├── dev/                              # 🔧 DEVELOPMENT TOOLS
│   ├── scripts/
│   │   ├── read-profile.py           # TTS character reading
│   │   ├── parse-chat-sessions.py    # VS Code chat session extraction
│   │   ├── daily-session-summary.sh  # Automated development tracking
│   │   └── setup-daily-summaries.sh  # Session automation setup
│   ├── workflows/
│   │   ├── commit-local.md
│   │   ├── process-episode.md
│   │   └── text-to-speech.md
│   ├── config/
│   │   └── tts-config.json          # TTS voice configuration
│   ├── docs/
│   │   ├── project-structure.md
│   │   └── development-guide.md
│   ├── logs/
│   │   └── conversation-summaries/   # Automated session tracking
│   │       ├── README.md             # System documentation
│   │       ├── YYYY-MM/              # Monthly directories (e.g., 2025-07/, 2025-08/)
│   │       │   └── YYYY-MM-DD-session.md # Daily session summaries
│   │       └── automation-heartbeat.log # System activity log
│   └── cache/
│       └── audio-cache/             # TTS generated audio files
├── Makefile                          # 🔧 AUTOMATION
├── README.md                         # 📖 PROJECT OVERVIEW
├── series-bible.md                   # 📚 CREATIVE GUIDELINES
├── .gitignore                        # 🔧 VERSION CONTROL
└── .rclone-filter                   # 🔧 SYNC CONFIGURATION
```

## Structure Overview

This project uses a **separated concerns** approach with three main areas:

### 🎭 Creative Content (`content/`)
All creative assets, character definitions, and story content organized for easy navigation and collaboration.

### 🎬 Final Deliverables (`production/`)
Complete episodes ready for YouTube upload, with metadata tracking and video files managed via hybrid Git + Google Drive workflow.

### 🔧 Development Tools (`dev/`)
Scripts, automation, configuration, and documentation for the technical development process.

## Detailed Organization

### content/ - Creative Content
- **assets/**: All creative assets organized by type
  - **images/**: Visual assets organized by character and scene type
    - `background/`: Scene backgrounds organized by location and context (25 total images)
      - `school-buildings/`: Exterior school views (3 images)
      - `classroom/`: Interior classroom elements (6 images)
      - `principal-office/`: Principal's office furniture and decor (4 images)
      - `playground/`: Outdoor play equipment and areas (4 images)
      - `characters/`: Teacher and authority figure images (2 images)
        - chemistry-teacher.png, science-teacher.png
      - `nature/`: Natural elements like flowers, animals, weather (3 images)
      - `props/`: Standalone objects and transportation (3 images)
    - `glove/`: Individual images of Glove character (3 expressions)
    - `mitten/`: Individual images of Mitten character (5 expressions)  
    - `gloveandmitten/`: Images featuring both main characters together (3 sample images)
  - **audio/**: Reusable audio elements (intros, outros, sound effects library)
    - Reserved for shared audio assets that can be used across multiple episodes
    - Episode-specific audio files remain with their respective stories
  - **templates/**: Series-wide branding and production templates
    - Reserved for cross-saga elements (intro/outro cards, title templates, end cards)
    - Generic episode frameworks and production workflow templates
    - Saga-specific episode templates remain with their respective sagas
- **characters/**: Character definitions and backstories organized by scope
  - **main/**: Universal characters appearing across all sagas (Glove, Mitten, Fingers-and-Hand)
  - **sagas/**: Saga-specific supporting characters
    - `school-daze/`: Principal Watch, Instructor Beaker (school environment characters)
    - `mis-adventures/`: Future supporting characters for comedy storylines
- **stories/**: All story content organized by development stage
  - **ideas/**: Single episode concepts and brainstorming
    - `mis-adventures/`: Comedy episode concepts
    - `school-daze/`: Educational episode concepts
  - **sagas/**: Multi-episode story arcs with deeper nesting for episode organization
    - `mis-adventures/stories/`: Extended comedy storylines
    - `school-daze/stories/`: Educational story arcs
      - `lights/`: Learning and discovery storylines
        - `tuff-daze/`: Challenge-focused episodes within lights saga

### production/ - Final Deliverables
- **Hybrid YouTube production workflow** (Git + Google Drive)
  - `completed/metadata/`: Episode metadata, descriptions, tags, upload checklists (Git-tracked)
  - `completed/videos/`: Final MP4 exports ready for upload (Google Drive only)
  - `in-progress/`: Work-in-progress renders and drafts (Google Drive only)
  - `README.md`: Production workflow documentation

### dev/ - Development Tools
- **scripts/**: Automation scripts and development utilities
  - `read-profile.py`: Google Cloud TTS character profile audio generation
  - `parse-chat-sessions.py`: VS Code chat session extraction and processing
  - `daily-session-summary.sh`: Automated development session tracking
  - `setup-daily-summaries.sh`: Installation and management of session automation
- **workflows/**: Process documentation
  - `commit-local.md`: Git commit + Google Drive sync workflow  
  - `process-episode.md`: PowerPoint → PDF → YouTube metadata automation
  - `text-to-speech.md`: TTS character profile reading workflow
- **config/**: Configuration files
  - `tts-config.json`: Google Cloud TTS voice and audio settings
- **docs/**: Development documentation
  - `project-structure.md`: This documentation
  - `development-guide.md`: How to use development tools
- **logs/**: Automated development tracking
  - `conversation-summaries/`: VS Code chat session summaries and daily session tracking
    - `README.md`: Chat automation system documentation
    - `YYYY-MM/`: Monthly directories containing session files (e.g., `2025-07/`, `2025-08/`)
    - `YYYY-MM-DD-session.md`: Daily development session summaries with accurate timestamps
- **cache/**: Temporary files (audio cache, not synced)

### Root Files
- `Makefile`: Simple command interface for all workflows
- `README.md`: Project overview and quick start guide
- `series-bible.md`: Character rules and creative guidelines
- `.gitignore`: Version control exclusions
- `.rclone-filter`: Google Drive sync exclusions

## Current Content Inventory

### Creative Assets
- **Audio Files**: Episode-specific audio (4-scene structure) stored with their respective stories
  - Example: scene-one.mp3 through scene-four.mp3 in `content/stories/sagas/school-daze/stories/lights/tuff-daze/`
  - Reusable audio elements (intros, sound effects) stored in `content/assets/audio/` when created
- **Visual Assets**: 25 background images organized by scene type in `content/assets/images/background/`
  - Character expressions for Glove (3) and Mitten (5) in respective character folders
  - Combined character images (3) in `gloveandmitten/` folder
- **PowerPoint Templates**: Saga-specific episode templates stored with their sagas
  - `mis-adventures/episode-template.pptx` and `school-daze/episode-template.pptx`
  - Series-wide templates (branding, production tools) stored in `content/assets/templates/` when created

### Development Tools
- **TTS System**: Google Cloud Text-to-Speech with character voice generation
  - Configuration in `dev/config/tts-config.json`
  - Audio cache in `dev/cache/audio-cache/` (excluded from sync)
  - Scripts in `dev/scripts/read-profile.py`
- **Chat Automation**: VS Code integration for development session tracking
  - Chat session extraction via `dev/scripts/parse-chat-sessions.py`
  - Automated daily summaries via `dev/scripts/daily-session-summary.sh`
  - Historical development tracking in `dev/logs/conversation-summaries/`
- **Automation**: Makefile-based workflow commands
- **Documentation**: Comprehensive guides in `dev/docs/`

### Production Status
- **Existing Episodes**: Complete "Lights" story with "Tuff Daze" episode in school-daze saga
- **Metadata**: Episode upload information and templates in `production/completed/metadata/`
- **Story Pipeline**: Ideas and completed stories organized by saga type in `content/stories/`

## Benefits of This Structure

### 🎭 Creative Benefits
- **Clean workspace**: Content creators see only creative files
- **Logical organization**: Stories, characters, and assets grouped intuitively
- **Easy collaboration**: Non-technical team members can focus on content

### 🔧 Technical Benefits
- **Separated concerns**: Development tools don't clutter creative workspace
- **Centralized configuration**: All technical settings in one location
- **Efficient caching**: Temporary files grouped and properly excluded
- **Clear automation**: Simple Makefile interface to complex workflows
- **Development tracking**: Automated session summaries preserve context and decisions
- **AI integration**: VS Code chat sessions captured for project history

### 🎬 Production Benefits
- **Hybrid workflow**: Git for metadata, Google Drive for large video files
- **Version control**: Track episode information without huge file sizes
- **Upload ready**: Final deliverables organized for YouTube workflow
