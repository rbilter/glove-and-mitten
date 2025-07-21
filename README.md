# Glove and Mitten

A creative project for developing YouTube episodes featuring the characters Glove and Mitten in their adventures.

## Getting Started

1. Read [Series Bible](content/series-bible.md) for character guidelines
2. Explore [Project Structure](dev/docs/project-structure.md) for organization
3. Use `make help` to see available automation commands
4. Start creating episodes using saga templates in `content/stories/sagas/`

## Project Overview

This repository contains all source materials, workflows, and production assets for creating educational and entertaining episodes featuring:
- **Glove** - Adventure-seeking character
- **Mitten** - Social media enthusiast  
- **Supporting Cast** - Principal Watch, Instructor Beaker, and the "Mittenites"

## Quick Start

### Creating New Episodes
1. **Create PowerPoint** using saga templates in `content/stories/sagas/[saga]/`
2. **Run process-episode** workflow to generate YouTube metadata
3. **Export final video** to `production/completed/videos/`

### Automation Commands
```bash
# Using Makefile interface (recommended)
make help                    # Show all available commands
make process-episode EPISODE=path/to/episode.pptx
make commit-local           # Commit changes and sync to Google Drive  
make sync                   # Alias for commit-local
make status                 # Show project status

# Direct workflow access
dev/workflows/process-episode.md     # Episode processing workflow
dev/workflows/commit-local.md        # Git + GitHub + Google Drive sync
```

## Project Structure

### 📁 Core Directories
- **`content/characters/`** - Character definitions (main cast + saga-specific)  
- **`content/stories/`** - Episode ideas and completed story arcs
- **`content/assets/`** - Images, audio, and templates organized by type
- **`production/`** - Final deliverables and YouTube metadata
- **`dev/workflows/`** - Automation documentation and processes
- **`dev/scripts/`** - TTS tools and automation scripts

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
- **[Process Episode](workflows/process-episode.md)** - PowerPoint → PDF → YouTube metadata
- **[Commit Local](workflows/commit-local.md)** - Git + GitHub + Google Drive sync

## Stats

- **170 directories** with organized creative assets
- **234 files** including episodes, characters, documentation, and media assets
- **10 markdown files** for comprehensive documentation
- **Hybrid workflow** combining Git version control with Google Drive cloud sync
- **Automated metadata** generation from actual episode content
- **GitHub integration** with SSH remote for collaboration

## Development Workflow

1. **Create Episodes** using PowerPoint templates in saga directories
2. **Process Episodes** with `make process-episode` to generate metadata
3. **Commit Changes** with `make commit-local` for Git + Google Drive sync
4. **Collaborate** via GitHub repository with automatic cloud backup

Ready to bring Glove and Mitten's adventures to life! 🎬
