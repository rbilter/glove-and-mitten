# Commit Local Changes Workflow

## Overview
Ensures local changes are properly committed to Git and synchronized with Google Drive, keeping all three environments (local, Git, Google Drive) in sync.

## Usage
**Commands:** 
- `make commit-local` (primary command)
- `make sync` (alias for commit-local)

**Natural Language:**
- "Commit local changes and sync"
- "Run commit-local workflow"
- "Run sync workflow"
- "Sync my local work to git and google drive"

## What commit-local Does Automatically:
1. ✅ **Checks local status** - Shows what files have changed
2. ✅ **Stages all changes** to Git
3. ✅ **Commits with descriptive message** based on actual changes
4. ✅ **Syncs to Google Drive** via rclone
5. ✅ **Verifies sync status** and reports any issues

## Workflow Steps

### Phase 1: Local Assessment
1. **Check Git Status**
   ```bash
   git status --porcelain
   ```

2. **Show Changes Summary**
   - New files created
   - Modified files
   - Deleted files

### Phase 2: Git Operations
3. **Stage All Changes**
   ```bash
   git add -A
   ```

4. **Generate Smart Commit Message**
   - Analyze what types of files changed
   - Create descriptive commit message
   - Include date and change summary

5. **Commit Changes**
   ```bash
   git commit -m "[Generated message based on changes]"
   ```

### Phase 3: Google Drive Sync
6. **Sync to Google Drive**
   ```bash
   rclone sync . gdrive:glove-and-mitten --exclude .git/ --progress
   ```

7. **Verify Sync**
   ```bash
   rclone check . gdrive:glove-and-mitten --exclude .git/
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
