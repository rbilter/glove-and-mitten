#!/bin/bash
# Daily Session Summary Generator
# Automatically creates session summaries based on git activity

set -e

# Configuration
REPO_DIR="/home/rbilter/work/repos/glove-and-mitten"
SUMMARY_DIR="$REPO_DIR/dev/logs/conversation-summaries"
TODAY=$(date +%Y-%m-%d)
DELTA_FILE="$SUMMARY_DIR/$TODAY-session.md"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to log with timestamp
log() {
    echo -e "[$(date '+%H:%M:%S')] $1"
}

# Function to check if we're in the right directory
check_repo() {
    cd "$REPO_DIR" || {
        log "${RED}❌ Cannot access repository directory: $REPO_DIR${NC}"
        exit 1
    }
    
    if [ ! -d ".git" ]; then
        log "${RED}❌ Not a git repository: $REPO_DIR${NC}"
        exit 1
    fi
}

# Function to detect git activity today
detect_activity() {
    local today_commits
    local today_changes
    
    # Check for commits today
    today_commits=$(git log --since="00:00" --until="23:59" --oneline 2>/dev/null | wc -l)
    
    # Check for uncommitted changes
    today_changes=$(git status --porcelain 2>/dev/null | wc -l)
    
    if [ "$today_commits" -gt 0 ] || [ "$today_changes" -gt 0 ]; then
        return 0  # Activity detected
    else
        return 1  # No activity
    fi
}

# Function to get git activity summary
get_git_summary() {
    echo "## 📊 Git Activity"
    echo ""
    
    # Today's commits
    local commits
    commits=$(git log --since="00:00" --until="23:59" --oneline 2>/dev/null)
    if [ -n "$commits" ]; then
        echo "### Commits Made Today:"
        echo '```'
        echo "$commits"
        echo '```'
        echo ""
    fi
    
    # Current status
    local status
    status=$(git status --porcelain 2>/dev/null)
    if [ -n "$status" ]; then
        echo "### Uncommitted Changes:"
        echo '```'
        echo "$status"
        echo '```'
        echo ""
    fi
    
    # Recent file modifications
    echo "### Recently Modified Files:"
    echo '```'
    git diff --name-only HEAD~1 2>/dev/null || echo "No recent changes"
    echo '```'
    echo ""
}

# Function to create active session summary
create_active_summary() {
    log "${GREEN}📝 Creating active session summary...${NC}"
    
    cat > "$DELTA_FILE" << EOF
# Session Summary - $TODAY
*Changes and additions since baseline session*

## 📅 Session Info
- **Date**: $TODAY
- **Previous Baseline**: $(ls -t "$SUMMARY_DIR"/*baseline.md 2>/dev/null | head -1 | xargs basename 2>/dev/null || echo "No baseline found")
- **Session Type**: Active Development Session
- **Auto-Generated**: $(date '+%Y-%m-%d %H:%M:%S')

$(get_git_summary)

## 🔄 Session Activity
*This summary was auto-generated. Manual updates can be added below.*

### Tasks Worked On
- [ ] *Add tasks worked on today*

### Files Modified
- See git activity above

### Decisions Made
- *Add key decisions made during the session*

### Problems Solved
- *Add problems encountered and how they were resolved*

### Ideas Discussed
- *Add new ideas or approaches discussed*

## ⏭️ For Next Session
- *Add goals and action items for next session*

## 💭 Notes
- *Add any additional context or observations*

---
*Auto-generated on $TODAY at $(date '+%H:%M:%S'). Edit this file to add manual session details.*
EOF
}

# Function to create no-session summary
create_no_session_summary() {
    log "${YELLOW}📝 Creating no-session summary...${NC}"
    
    cat > "$DELTA_FILE" << EOF
# Session Summary - $TODAY
*No development session detected*

## 📅 Session Info
- **Date**: $TODAY
- **Previous Baseline**: $(ls -t "$SUMMARY_DIR"/*baseline.md 2>/dev/null | head -1 | xargs basename 2>/dev/null || echo "No baseline found")
- **Session Type**: No Session
- **Auto-Generated**: $(date '+%Y-%m-%d %H:%M:%S')

## 🚫 No Activity Detected
- No git commits made today
- No uncommitted changes detected
- No development session occurred

## 📊 Repository Status
- **Last Commit**: $(git log -1 --format="%h - %s (%cr)" 2>/dev/null || echo "No commits found")
- **Branch**: $(git branch --show-current 2>/dev/null || echo "Unknown")
- **Status**: $(git status --porcelain 2>/dev/null | wc -l) uncommitted changes

## ⏭️ Next Session
- Resume work when ready
- Check recent deltas for context

---
*Auto-generated on $TODAY at $(date '+%H:%M:%S'). No development activity detected.*
EOF
}

# Function to update existing delta file
update_existing_summary() {
    log "${YELLOW}📝 Delta file already exists, updating with latest git info...${NC}"
    
    # Backup existing file
    cp "$DELTA_FILE" "$DELTA_FILE.backup"
    
    # Update the git activity section
    local temp_file
    temp_file=$(mktemp)
    
    # Extract everything before git activity section
    sed '/## 📊 Git Activity/,$d' "$DELTA_FILE" > "$temp_file"
    
    # Add updated git activity
    get_git_summary >> "$temp_file"
    
    # Add everything after git activity section (if it exists)
    sed -n '/## 🔄 Session Activity/,$p' "$DELTA_FILE" >> "$temp_file"
    
    # Replace original file
    mv "$temp_file" "$DELTA_FILE"
    
    log "${GREEN}✅ Updated existing delta file with latest git activity${NC}"
}

# Main execution
main() {
    log "${GREEN}🤖 Daily Session Summary Generator${NC}"
    log "📅 Date: $TODAY"
    
    # Check repository
    check_repo
    
    # Create summary directory if it doesn't exist
    mkdir -p "$SUMMARY_DIR"
    
    # Check if delta file already exists
    if [ -f "$DELTA_FILE" ]; then
        update_existing_summary
        return 0
    fi
    
    # Detect activity and create appropriate summary
    if detect_activity; then
        log "${GREEN}🎯 Development activity detected${NC}"
        create_active_summary
    else
        log "${YELLOW}😴 No development activity detected${NC}"
        create_no_session_summary
    fi
    
    log "${GREEN}✅ Summary created: $DELTA_FILE${NC}"
    
    # Show summary stats
    log "📊 Summary contains $(wc -l < "$DELTA_FILE") lines"
}

# Run main function
main "$@"
