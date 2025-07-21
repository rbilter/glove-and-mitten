# Episode Production Workflow: process-episode

## Overview
The `process-episode` workflow automatically generates YouTube metadata from completed PowerPoint episodes, ensuring descriptions are based on actual episode content rather than assumptions.

## Usage
**Command:** `make process-episode EPISODE=path/to/episode.pptx`

**Example:**
```bash
make process-episode EPISODE=content/stories/sagas/school-daze/stories/lights/tuff-daze/01-lights-tuff-daze-episode.pptx
```

**Assistant Integration:**
- "Process episode: [episode-path]"
- "Run process-episode on the tuff-daze episode" 
- "Generate metadata for episode 01-lights-tuff-daze"

## What process-episode Does Automatically:
1. ✅ **Generates PDF** from your completed PowerPoint
2. ✅ **Extracts episode content** (dialog, scenes, characters)
3. ✅ **Creates metadata folder** with proper naming convention
4. ✅ **Generates description.md** based on actual story content
5. ✅ **Creates optimized tags.txt** for YouTube search
6. ✅ **Sets up upload-checklist.md** with episode-specific details
7. ✅ **Reports completion** with file locations

## Complete Workflow Steps

### Phase 1: Episode Creation
1. **Create Episode PowerPoint**
   - Use saga-specific template from `content/stories/sagas/[saga]/episode-template.pptx`
   - Save as `##-[story]-[episode].pptx` in story folder
   - Include all dialog, scenes, and visual content

2. **Generate PDF from PowerPoint (Automated)**
   - System automatically converts PowerPoint to PDF
   - PDF saved in same folder with same naming convention
   - Command: `libreoffice --headless --convert-to pdf --outdir [story-folder] [episode].pptx`
   - This PDF becomes the source for description generation

3. **Render Final Video**
   - Export PowerPoint to MP4 format
   - Save to `production/completed/videos/`
   - Use naming convention: `##-[Story]-[Episode].mp4`

### Phase 2: Automated Metadata Generation
4. **Extract Episode Content**
   ```bash
   pdftotext path/to/episode.pdf -
   ```

5. **Generate Episode Metadata**
   - Create folder: `production/completed/metadata/##-[story]-[episode]/`
   - Generate `description.md` based on PDF content
   - Generate `tags.txt` with relevant keywords
   - Create `upload-checklist.md` from template

6. **Update Project Documentation**
   - Mark episode as completed in project structure
   - Update any story arc status files

### Phase 3: Upload Preparation
7. **Review Generated Content**
   - Check description accuracy against actual episode
   - Verify tags are appropriate and optimized
   - Complete upload checklist verification

8. **Upload to YouTube**
   - Use generated description and tags
   - Follow checklist for all settings
   - Add to appropriate playlists

## File Organization Example
```
content/stories/sagas/school-daze/stories/lights/tuff-daze/
├── 01-lights-tuff-daze-episode.pptx    # Source
├── 01-lights-tuff-daze-episode.pdf     # For description generation
├── scene-one.mp3                       # Audio assets
├── scene-two.mp3
├── scene-three.mp3
└── scene-four.mp3

production/completed/videos/
└── 01-Lights-Tuff-Daze.mp4            # Final video

production/completed/metadata/01-lights-tuff-daze/
├── description.md                       # Generated from PDF
├── tags.txt                            # Generated keywords
└── upload-checklist.md                 # Upload verification
```

## Automated Commands

### Generate PDF from PowerPoint
```bash
libreoffice --headless --convert-to pdf --outdir content/stories/sagas/[saga]/stories/[story]/[episode]/ content/stories/sagas/[saga]/stories/[story]/[episode]/##-[story]-[episode].pptx
```

### Extract Episode Content
```bash
pdftotext content/stories/sagas/[saga]/stories/[story]/[episode]/##-[story]-[episode].pdf -
```

### Create Metadata Folder
```bash
mkdir -p production/completed/metadata/##-[story]-[episode]
```

### Generate Description Template
```bash
cp production/completed/metadata/templates/description-template.md production/completed/metadata/##-[story]-[episode]/description.md
```

## Quality Assurance
- PDF content accurately reflects PowerPoint slides
- Generated descriptions create intrigue without spoiling plot
- Tags optimize for target audience and educational content
- Upload checklist ensures consistent quality standards

## Benefits
- **Consistency**: Standardized process for all episodes
- **Accuracy**: Descriptions based on actual content, not assumptions
- **Efficiency**: Automated metadata generation saves time
- **Quality**: Checklist ensures nothing is missed before upload
- **Version Control**: All source materials tracked in git

## Notes
- PDFs are kept in git (typically 1-2MB, manageable size)
- PowerPoint files serve as single source of truth
- Generated metadata can be manually refined if needed
- Workflow scales for multiple episodes and collaborators
