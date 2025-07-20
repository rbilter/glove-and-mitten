# Glove and Mitten

A creative project for developing YouTube episodes featuring the characters Glove and Mitten in their adventures at Accessory Academy.

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

### Process Episode Automation
```bash
# Tell the assistant: "Process episode: [path-to-episode.pptx]"
# Automatically generates PDF, extracts content, creates YouTube metadata
```

## Project Structure

### 📁 Core Directories
- **`assets/`** - Images, audio, and templates organized by type
- **`characters/`** - Character definitions (main cast + saga-specific)
- **`stories/`** - Episode ideas and completed story arcs
- **`production/`** - YouTube workflow and metadata

### 🎬 Current Episodes
- **Episode 01: Lights - Tuff Daze** ✅ Complete with metadata

## Workflows

### Episode Production
1. **Creative** - PowerPoint episode creation
2. **Automated** - PDF generation and metadata extraction  
3. **Upload** - YouTube preparation with generated descriptions

### File Management
- **Git** - Source files, metadata, documentation
- **Google Drive** - Large video files and collaboration

## Documentation

- **[Project Structure](project-structure.md)** - Complete folder organization
- **[Series Bible](series-bible.md)** - Character rules and world-building
- **[Production Workflow](production/WORKFLOW.md)** - process-episode automation
- **[Production Guide](production/README.md)** - YouTube workflow

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
