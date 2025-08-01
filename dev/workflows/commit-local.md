# Commit Local Changes Workflow

## Overview
Ensures local changes are properly committed to Git and synchronized with Google Drive, keeping all three environments (local, Git, Google Drive) in sync.

## Usage
**Natural Language Commands:**

**Assistant Integration:**
- "Commit local changes and sync"
- "Run commit-local workflow"
- "Run sync workflow"
- "Sync my local work to git and google drive"

## What commit-local Does Automatically:
1. ✅ **Checks local status** - Shows what files have changed
2. ✅ **Stages all changes** to Git
3. ✅ **Commits with descriptive message** based on actual changes
4. ✅ **Pushes to GitHub** - Updates remote repository
5. ✅ **Syncs to Google Drive** - Excludes unnecessary files via `.rclone-filter`
6. ✅ **Verifies sync integrity** - Ensures backup is complete

## File Exclusions
The `.rclone-filter` file controls what gets synced to Google Drive:
- **Excluded:** `.venv/`, `__pycache__/`, `scripts/audio-cache/`, build artifacts
- **Included:** Source code, documentation, character profiles, workflows
4. ✅ **Pushes to remote repository** (GitHub)
5. ✅ **Syncs to Google Drive** via rclone
6. ✅ **Verifies sync status** and reports any issues

## Workflow Steps

### Phase 1: Local Assessment
1. **Check Git Status**
   ```bash
   git status --porcelain
   ```

2. **Show Changes Summary**
   - New files created (untracked files marked with ??)
   - Modified files (marked with M)
   - Deleted files (marked with D)
   - Staged files (marked with A)

3. **Verify All File Types**
   - ✅ **Staged changes**: Already ready for commit
   - ✅ **Unstaged changes**: Modified tracked files
   - ✅ **Untracked files**: New files not yet in git (IMPORTANT: Don't miss these!)

### Phase 2: Git Operations
4. **Stage All Changes Including Untracked Files**
   ```bash
   git add -A  # Includes untracked files, modifications, and deletions
   ```

5. **Generate Smart Commit Message**
   - Analyze what types of files changed
   - Create descriptive commit message
   - Include date and change summary

6. **Commit Changes**
   
   **Option A: Single-line message (recommended for automation)**
   ```bash
   git commit -m "[Generated message based on changes]"
   ```
   
   **Option B: Multi-line message (use multiple -m flags)**
   ```bash
   git commit -m "Summary of changes" -m "- Detailed point 1" -m "- Detailed point 2"
   ```
   
   **⚠️ Important:** Avoid embedded newlines in `-m` strings as they can cause git to hang:
   ```bash
   # DON'T DO THIS (hangs):
   git commit -m "Title
   
   Body with details"
   ```

7. **Verify Commit Success**
   ```bash
   git log -1 --oneline  # Confirm commit was created
   ```

8. **Push to Remote Repository**
   ```bash
   git push origin main
   ```

9. **Verify Push Success**
   ```bash
   git status -b  # Confirm local branch is up to date with remote
   ```

### Phase 3: Google Drive Sync
10. **Sync to Google Drive**
   ```bash
   rclone sync . gdrive:glove-and-mitten --filter-from .rclone-filter --progress
   ```

11. **Verify Sync**
   ```bash
   rclone check . gdrive:glove-and-mitten --filter-from .rclone-filter
   ```

## Use Cases
- **After creating new episodes** - Commit PowerPoint files, metadata
- **After updating documentation** - Sync README, workflow changes  
- **After organizing assets** - Commit new images, audio files
- **End of work session** - Ensure everything is backed up

## Example Commit Messages
- "Add Episode 02 metadata and PowerPoint source"
- "Update character definitions and series bible"  
- "Reorganize assets and fix workflow documentation"
- "Daily sync: new ideas and template updates"

## Safety Features
- **Dry-run preview** - Shows what would sync before actual operation
- **Error handling** - Reports Git conflicts or rclone issues
- **Status verification** - Confirms sync completed successfully
- **Backup check** - Verifies Google Drive has latest files
