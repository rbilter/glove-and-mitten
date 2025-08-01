# Production Workflow

## Overview
The production folder uses a hybrid approach combining Git version control with Google Drive sync for optimal collaboration and file management.

## File Organization Strategy

### Git-Tracked Files (Lightweight)
- `production/completed/metadata/` - Episode metadata, descriptions, tags, upload checklists
- `production/README.md` - This workflow documentation

### Google Drive Only (Large Files)
- `production/completed/videos/` - Final MP4 exports ready for YouTube upload
- `production/in-progress/` - Work-in-progress renders, drafts, temporary files

## Workflow

### 1. Episode Creation
1. Develop episode in `content/stories/sagas/[saga]/[story]/`
2. Create PowerPoint episode using saga template
3. Export/render video to `production/in-progress/`

### 2. Metadata Preparation
1. Create episode folder in `production/completed/metadata/`
2. Fill out metadata templates:
   - `description.md` - YouTube description text
   - `tags.txt` - Search tags and keywords
   - `upload-checklist.md` - Pre-upload verification

### 3. Final Production
1. Move final video from `in-progress/` to `completed/videos/`
2. Complete upload checklist
3. Upload to YouTube using metadata files

### 4. Sync Strategy
- **Git**: Handles metadata, documentation, and workflow files
- **Google Drive**: Handles all large video files and sharing
- **rclone**: Synchronizes Google Drive with local filesystem

## Metadata Templates

### Episode Folder Structure
```
production/completed/metadata/episode-###-[name]/
├── description.md      # YouTube description
├── tags.txt           # Search keywords
├── thumbnail-notes.md # Thumbnail creation notes
└── upload-checklist.md # Pre-upload verification
```

### Benefits
- **Git**: Version control for metadata, lightweight repo
- **Google Drive**: Easy sharing, collaboration on large files
- **Hybrid**: Best of both worlds for different file types
- **Scalable**: Works for single creator or team collaboration

## Quick Reference
- **Source files**: Stories and templates (Git)
- **Work in progress**: In-progress folder (Google Drive only)
- **Final videos**: Completed/videos folder (Google Drive only)
- **Upload data**: Completed/metadata folder (Git)

## Additional Documentation

- **Automation**: See `dev/workflows/process-episode.md` for episode processing
- **Sync workflow**: See `dev/workflows/commit-local.md` for Git+Google Drive sync
- **TTS System**: See `dev/workflows/text-to-speech.md` for character profile reading
- **Chat Automation**: See `dev/logs/conversation-summaries/README.md` for session tracking
- **Command interface**: Use `make help` to see all available automation commands
