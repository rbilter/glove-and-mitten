# Glove and Mitten

A creative project for developing YouTube episodes featuring the characters Glove and Mitten in their adventures.

## Getting Started

1. Read [Series Bible](content/series-bible.md) for character guidelines
2. Explore [Project Structure](dev/docs/project-structure.md) for organization
3. Use natural language commands with AI assistant for automation
4. Start creating episodes using saga templates in `content/stories/sagas/`

## Project Overview

This repository contains all source materials, workflows, and production assets for creating educational and entertaining episodes featuring:
- **Glove** - Methodical problem-solver and self-appointed security specialist
- **Mitten** - Warm-hearted social media enthusiast and community builder  
- **Supporting Cast** - Principal Watch, Instructor Beaker, and the "Mittenites"

## Quick Start

### Creating New Episodes
1. **Create PowerPoint** using saga templates in `content/stories/sagas/[saga]/`
2. **Run process-episode** workflow to generate YouTube metadata
3. **Export final video** to `production/completed/videos/`

### Automation Commands
```bash
# Natural language commands with AI assistant (recommended)
"commit-local"              # Commit changes and sync to Google Drive  
"process-episode: [path]"   # Process episode for metadata generation
"read-profile [character]"  # Text-to-speech for character profiles
"help"                      # Show all available commands
"status"                    # Show project status

# Direct workflow access
dev/workflows/process-episode.md     # Episode processing workflow
dev/workflows/commit-local.md        # Git + GitHub + Google Drive sync
dev/workflows/text-to-speech.md     # TTS character profile reading
```

## AI Assistant Guidelines (VS Code + GitHub Copilot)

### Core Workflow Commands
When working with AI assistants, use these exact trigger phrases:

**commit-local**: "commit-local", "run commit-local", "sync local changes"
- Execute: `dev/workflows/commit-local.md` workflow
- **ALWAYS run tests first**: `./dev/tests/run_tests.sh` (45 tests must pass)
- Steps: Test → Status → Stage → Commit → Push → Sync → Verify

**process-episode**: "process-episode", "Process episode: [path]"  
- Execute: `dev/workflows/process-episode.md` workflow
- Steps: Generate PDF → Extract content → Create metadata → Generate YouTube description

**text-to-speech**: "read-profile", "Read [character] profile", "Use TTS for [character]"
- Execute: `dev/workflows/text-to-speech.md` workflow  
- Script: `dev/scripts/markdown-tts.py`
- Steps: Clean markdown → Google Cloud TTS → Play/save audio → Cache results

**utility-commands**: "help", "status", "clean", "list characters", "list voices"
- Show project information and utilities
- Commands: "help" (show workflows), "status" (git status), "clean" (remove cache), "list characters" (TTS profiles), "list voices" (Google TTS voices)

### Content Guidelines
- **Character consistency**: Glove (practical, organized), Mitten (warm-hearted, creative)
- **Family-friendly PG content** with realistic character conflicts
- **Episode format**: 3-5 panel comic style, 60-120 second duration, 4-scene structure
- **Educational themes** with character-building focus

### Project Structure Rules
- **Character files**: `content/characters/main/` or `content/characters/sagas/[saga-name]/`
- **Episode naming**: `##-[story]-[episode].pptx` (e.g., `01-lights-tuff-daze-episode.pptx`)
- **Monthly directories**: `YYYY-MM/` format (e.g., `2025-07/`, `2025-08/`)
- **Test suite**: 45 comprehensive tests covering all automation scripts
- **Production workflow**: Metadata in git, large files (videos) Google Drive only

### Automation Systems
- **PowerPoint → PDF**: Automated conversion via LibreOffice
- **Content extraction**: pdftotext for dialogue and content
- **Metadata generation**: YouTube description, tags, upload checklist
- **Chat sessions**: Automatically parsed and included in daily summaries

### Development Environment
- **Python virtual environment**: `.venv/` (auto-configured)
- **Testing framework**: `./dev/tests/run_tests.sh` 
- **Required tools**: rclone, LibreOffice, pdftotext, Python 3, Google Cloud TTS
- **Git workflow**: Tests → Commit → Push → Sync to Google Drive

### AI Behavioral Rules
1. **Follow existing workflows exactly** - Don't create ad-hoc processes
2. **Run tests before commits** - All 45 tests must pass via `./dev/tests/run_tests.sh`
3. **Use documented file locations** - Respect established structure
4. **Check existing files** before creating new ones
5. **Terminal commands must be single-line** - Use `&&` or `;` operators
6. **Always verify operations** - Use status checks after git and sync operations
7. **Preserve user's naming conventions** - Don't change established patterns
8. **Use hybrid production approach** - Source files in git, large outputs Google Drive only

## Project Structure

### 📁 Core Directories
- **`content/characters/`** - Character definitions (main cast + saga-specific)  
- **`content/stories/`** - Episode ideas and completed story arcs
- **`content/assets/`** - Images, audio, and templates organized by type
- **`production/`** - Final deliverables and YouTube metadata
- **`dev/workflows/`** - Automation documentation and processes
- **`dev/scripts/`** - TTS tools, chat automation, and workflow scripts
- **`dev/logs/`** - Automated conversation summaries and development tracking

### 🎬 Current Episodes
- **Episode 01: Lights - Tuff Daze** ✅ Complete with metadata

## Workflows

### Episode Creation Process
1. **Develop Story** in `stories/ideas/` or use existing saga concepts
2. **Create Episode** using PowerPoint templates in `content/stories/sagas/[saga]/`  
3. **Process Episode** using automation workflow
4. **Export Video** and save to `production/completed/videos/`
5. **Upload to YouTube** using generated metadata

### Automation Workflows
- **[Process Episode](dev/workflows/process-episode.md)** - PowerPoint → PDF → YouTube metadata
- **[Commit Local](dev/workflows/commit-local.md)** - Git + GitHub + Google Drive sync
- **[Text-to-Speech](dev/workflows/text-to-speech.md)** - Character profile audio reading
- **[Chat Automation](dev/logs/conversation-summaries/README.md)** - Automated development session tracking

## Stats

- **50 directories** with organized creative and development assets
- **97 project files** including episodes, characters, documentation, and automation scripts
- **28 markdown files** for comprehensive documentation and session tracking
- **Hybrid workflow** combining Git version control with Google Drive cloud sync
- **Automated metadata** generation from actual episode content
- **GitHub integration** with SSH remote for collaboration
- **Chat automation** with VS Code integration for development session tracking
- **TTS system** for character profile audio generation using Google Cloud

## Development Workflow

1. **Create Episodes** using PowerPoint templates in saga directories
2. **Process Episodes** with "process-episode: [path]" to generate metadata
3. **Track Progress** via automated conversation summaries and session logs
4. **Commit Changes** with "commit-local" for Git + Google Drive sync
5. **Collaborate** via GitHub repository with automatic cloud backup

Ready to bring Glove and Mitten's adventures to life! 🎬
