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
1. ✅ **Validates automation** - Runs comprehensive test suite (45 tests)
2. ✅ **Checks local status** - Shows what files have changed
3. ✅ **Stages all changes** to Git
4. ✅ **Commits with descriptive message** based on actual changes
5. ✅ **Pushes to GitHub** - Updates remote repository
6. ✅ **Syncs to Google Drive** - Excludes unnecessary files via `.rclone-filter`
7. ✅ **Verifies sync integrity** - Ensures backup is complete

## File Exclusions
The `.rclone-filter` file controls what gets synced to Google Drive:
- **Excluded:** `.venv/`, `__pycache__/`, `scripts/audio-cache/`, build artifacts
- **Included:** Source code, documentation, character profiles, workflows
4. ✅ **Pushes to remote repository** (GitHub)
5. ✅ **Syncs to Google Drive** via rclone
6. ✅ **Verifies sync status** and reports any issues

## Executable Steps

Execute these commands in order:

1. **Run Test Suite** (⚠️ HALT if any tests fail)
   ```bash
   ./dev/tests/run_tests.sh
   ```

2. **Check Git Status**
   ```bash
   git status --porcelain
   ```

3. **Stage All Changes**
   ```bash
   git add -A
   ```

4. **Commit Changes** (use multiple -m flags, never multi-line strings)
   ```bash
   git commit -m "Summary of changes" -m "Detail 1" -m "Detail 2"
   ```

5. **Verify Commit**
   ```bash
   git log -1 --oneline
   ```

6. **Push to Remote**
   ```bash
   git push origin main
   ```

7. **Verify Push**
   ```bash
   git status -b
   ```

8. **Sync to Google Drive**
   ```bash
   rclone sync . gdrive:glove-and-mitten --filter-from .rclone-filter --progress
   ```

9. **Verify Sync**
   ```bash
   rclone check . gdrive:glove-and-mitten --filter-from .rclone-filter
   ```

## Test Failure Protocol

**If `./dev/tests/run_tests.sh` fails:**

1. **Review test output** - Identify which specific tests failed
2. **Investigate root cause:**
   - **Code change broke functionality** → Fix the automation scripts
   - **Test needs updating** → Update test expectations if behavior intentionally changed
   - **Environment issue** → Check dependencies, file permissions, git state
3. **Re-run tests** until all 45 tests pass
4. **Only proceed with commit** after full test suite passes

**Common test failure causes:**
- Missing dependencies in `.venv`
- Changed function signatures in automation scripts  
- File permission issues on test scripts
- Git repository state affecting shell script tests

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
