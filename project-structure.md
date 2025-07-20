# Project Structure Plan

## Implemented Folder Structure

```
glove-and-mitten/
├── assets/
│   ├── images/
│   │   ├── background/
│   │   │   ├── school-buildings/
│   │   │   ├── classroom/
│   │   │   ├── principal-office/
│   │   │   ├── playground/
│   │   │   ├── characters/
│   │   │   ├── nature/
│   │   │   └── props/
│   │   ├── glove/
│   │   ├── gloveandmitten/
│   │   └── mitten/
│   ├── audio/
│   └── templates/
├── characters/
│   ├── main/
│   └── sagas/
│       ├── school-daze/
│       └── mis-adventures/
├── stories/
│   ├── ideas/
│   │   ├── mis-adventures/
│   │   └── school-daze/
│   ├── sagas/
│   │   ├── mis-adventures/
│   │   │   └── stories/
│   │   └── school-daze/
│   │       └── stories/
│   │           └── lights/
│   │               └── tuff-daze/
├── production/
│   ├── completed/
│   │   ├── metadata/
│   │   │   ├── 01-lights-tuff-daze/
│   │   │   └── templates/
│   │   └── videos/
│   ├── in-progress/
│   ├── README.md
│   └── WORKFLOW.md
├── README.md
├── project-structure.md
└── series-bible.md
```

## Notes
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
- **production/**: Hybrid YouTube production workflow (Git + Google Drive)
  - `completed/metadata/`: Episode metadata, descriptions, tags, upload checklists (Git-tracked)
  - `completed/videos/`: Final MP4 exports ready for upload (Google Drive only)
  - `in-progress/`: Work-in-progress renders and drafts (Google Drive only)
  - `README.md`: Production workflow documentation

## Current Content Inventory
- **Audio Files**: Episode-specific audio (4-scene structure) stored with their respective stories
  - Example: scene-one.mp3 through scene-four.mp3 in stories/sagas/school-daze/stories/lights/tuff-daze/
  - Reusable audio elements (intros, sound effects) will be stored in assets/audio/ when created
- **PowerPoint Templates**: Saga-specific episode templates stored with their sagas
  - mis-adventures/episode-template.pptx and school-daze/episode-template.pptx
  - Series-wide templates (branding, production tools) will be stored in assets/templates/ when created
- **Existing Episodes**: Complete "Lights" story with "Tuff Daze" episode in school-daze saga
- **Story Documents**: Ideas and completed stories organized by saga type

## Cleanup Tasks Needed
1. ✅ **Move back-stories files**: COMPLETED - Reorganized into new characters/ structure
2. ✅ **Remove empty root back-stories**: COMPLETED - Directory removed
3. ✅ **Create characters structure**: COMPLETED - Universal and saga-specific organization
4. ✅ **Implement production workflow**: COMPLETED - Hybrid Git+Google Drive approach
5. ✅ **Create process-episode automation**: COMPLETED - PDF generation and metadata workflow
6. ✅ **Complete Episode 01**: COMPLETED - Tuff Daze with full metadata package

## Status
✅ **Completed**: Project fully organized and production-ready!
🎯 **Ready**: Begin creating new episodes using established workflows!
