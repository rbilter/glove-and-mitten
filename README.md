# Glove and Mitten

A creative project for developing YouTube ep## Getting Started

1. Read [Series Bible](series-bible.md) for character guidelines
2. Explore [Project Structure](project-structure.md) for organization
3. Use `make help` to see available automation commands
4. Start creating episodes using saga templates in `stories/sagas/`s featuring the characters Glove and Mitten in their adventures at Accessory Academy.

## Project Overview

This repository contains all source materials, workflows, and production assets for creating educational and entertaining episodes featuring:
- **Glove** - Adventure-seeking character
- **Mitten** - Social media enthusiast  
- **Supporting Cast** - Principal Watch, Instructor Beaker, and the "Mittenites"

## Quick Start

### Creating New Episodes
1. **Create PowerPoint** using saga templates in `stories/sagas/[saga]/`
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

# Using natural language with assistant
# Tell the assistant: "Process episode: [path-to-episode.pptx]"
# Tell the assistant: "Run commit-local workflow"
```

## Project Structure

### 📁 Core Directories
- **`assets/`** - Images, audio, and templates organized by type
- **`characters/`** - Character definitions (main cast + saga-specific)
- **`stories/`** - Episode ideas and completed story arcs
- **`production/`** - YouTube workflow and metadata
- **`workflows/`** - Automation documentation and processes

### 🎬 Current Episodes
- **Episode 01: Lights - Tuff Daze** ✅ Complete with metadata

## Workflows

### Episode Creation Process
1. **Develop Story** in `stories/ideas/` or use existing saga concepts
2. **Create Episode** using PowerPoint templates in `stories/sagas/[saga]/`  
3. **Process Episode** using automation workflow
4. **Export Video** and save to `production/completed/videos/`
5. **Upload to YouTube** using generated metadata

### Automation Workflows
- **[Process Episode](workflows/process-episode.md)** - PowerPoint → PDF → YouTube metadata
- **[Commit Local](workflows/commit-local.md)** - Git commit + Google Drive sync

## Stats

- **39 directories** with organized creative assets
- **70 files** including episodes, characters, and documentation
- **Hybrid workflow** combining version control with cloud collaboration
- **Automated metadata** generation from actual episode content

## Getting Started

1. Review the [Series Bible](series-bible.md) for character guidelines
2. Check [Project Structure](project-structure.md) for organization
3. Use [Production Workflow](production/WORKFLOW.md) for episode creation
4. Start creating episodes in `stories/sagas/[saga]/stories/`

Ready to bring Glove and Mitten's adventures to life! 🎬
