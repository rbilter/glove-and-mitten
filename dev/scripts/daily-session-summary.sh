#!/bin/bash
# Daily Session Summary Generator
# Automatically creates session summaries based on git activity

set -e

# Configuration
REPO_DIR="/home/rbilter/work/repos/glove-and-mitten"
SUMMARY_DIR="$REPO_DIR/dev/logs/conversation-summaries"
# Use provided date or default to today
TARGET_DATE="${1:-$(date +%Y-%m-%d)}"
MONTH_DIR="$SUMMARY_DIR/$(date -d "$TARGET_DATE" +%Y-%m)"
DELTA_FILE="$MONTH_DIR/$TARGET_DATE-session.md"

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

# Function to ensure monthly directory exists
ensure_month_directory() {
    if [ ! -d "$MONTH_DIR" ]; then
        log "${YELLOW}📁 Creating monthly directory: $MONTH_DIR${NC}"
        mkdir -p "$MONTH_DIR" || {
            log "${RED}❌ Cannot create monthly directory: $MONTH_DIR${NC}"
            exit 1
        }
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

# Function to get chat conversations summary (as subsection)
get_chat_summary() {
    local chat_parser="$REPO_DIR/dev/scripts/parse-chat-sessions.py"
    
    # Check if chat parser exists and is executable
    if [ ! -x "$chat_parser" ]; then
        echo "### 💬 Chat Conversations"
        echo ""
        echo "*Chat parser not available or not executable*"
        echo ""
        return
    fi
    
    # Try to parse target date's chat sessions
    local chat_content
    chat_content=$(python3 "$chat_parser" --date "$TARGET_DATE" 2>/dev/null)
    
    if [ $? -eq 0 ] && [ -n "$chat_content" ]; then
        # Replace the main header with a subsection header
        echo "$chat_content" | sed 's/^## 💬 Chat Conversations/### 💬 Chat Conversations/'
        echo ""
    else
        echo "### 💬 Chat Conversations"
        echo ""
        echo "*No chat conversations found for today*"
        echo ""
    fi
}

# Function to get structured insights from chat
get_chat_insights() {
    local chat_parser="$REPO_DIR/dev/scripts/parse-chat-sessions.py"
    
    # Check if chat parser exists and is executable
    if [ ! -x "$chat_parser" ]; then
        return 1
    fi
    
    # Try to get structured insights from target date's chat sessions
    python3 "$chat_parser" --date "$TARGET_DATE" --format insights 2>/dev/null
}

# Function to populate session sections with chat insights
populate_sections_with_insights() {
    local insights_json="$1"
    
    if [ -z "$insights_json" ] || [ "$insights_json" = "null" ]; then
        # No insights available, return default template
        cat << 'EOF'
### Tasks Worked On
- [ ] *Add tasks worked on today*

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
EOF
        return
    fi
    
    # Extract insights using jq
    local tasks_worked_on=$(echo "$insights_json" | jq -r '.tasks_worked_on[]? // empty' 2>/dev/null)
    local decisions_made=$(echo "$insights_json" | jq -r '.decisions_made[]? // empty' 2>/dev/null)
    local problems_solved=$(echo "$insights_json" | jq -r '.problems_solved[]? // empty' 2>/dev/null)
    local ideas_discussed=$(echo "$insights_json" | jq -r '.ideas_discussed[]? // empty' 2>/dev/null)
    local for_next_session=$(echo "$insights_json" | jq -r '.for_next_session[]? // empty' 2>/dev/null)
    local notes=$(echo "$insights_json" | jq -r '.notes[]? // empty' 2>/dev/null)
    
    # Generate sections with insights
    echo "### Tasks Worked On"
    if [ -n "$tasks_worked_on" ]; then
        echo "$tasks_worked_on"
    else
        echo "- [ ] *Add tasks worked on today*"
    fi
    echo ""
    
    echo "### Decisions Made"
    if [ -n "$decisions_made" ]; then
        echo "$decisions_made"
    else
        echo "- *Add key decisions made during the session*"
    fi
    echo ""
    
    echo "### Problems Solved"
    if [ -n "$problems_solved" ]; then
        echo "$problems_solved"
    else
        echo "- *Add problems encountered and how they were resolved*"
    fi
    echo ""
    
    echo "### Ideas Discussed"
    if [ -n "$ideas_discussed" ]; then
        echo "$ideas_discussed"
    else
        echo "- *Add new ideas or approaches discussed*"
    fi
    echo ""
    
    echo "### ⏭️ For Next Session"
    if [ -n "$for_next_session" ]; then
        echo "$for_next_session"
    else
        echo "- *Add goals and action items for next session*"
    fi
    echo ""
    
    echo "### 💭 Notes"
    if [ -n "$notes" ]; then
        echo "$notes"
    else
        echo "- *Add any additional context or observations*"
    fi
    echo ""
    
    # Add chat conversations under Session Activity
    get_chat_summary | tail -n +2  # Skip the first line which is the header
}

# Function to create active session summary
create_active_summary() {
    log "${GREEN}📝 Creating active session summary...${NC}"
    
    # Get chat insights for structured sections
    local insights_json
    insights_json=$(get_chat_insights)
    
    cat > "$DELTA_FILE" << EOF
# Session Summary - $TODAY
*Changes and additions since baseline session*

## 📅 Session Info
- **Date**: $TARGET_DATE
- **Previous Baseline**: $(ls -t "$SUMMARY_DIR"/*baseline.md 2>/dev/null | head -1 | xargs basename 2>/dev/null || echo "No baseline found")
- **Session Type**: Active Development Session
- **Auto-Generated**: $(date '+%Y-%m-%d %H:%M:%S')

$(get_git_summary)

## 🔄 Session Activity
*This summary was auto-generated. Manual updates can be added below.*

$(populate_sections_with_insights "$insights_json")

---
*Auto-generated on $TODAY at $(date '+%H:%M:%S'). Edit this file to add manual session details.*
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
    
    # Add updated chat summary
    get_chat_summary >> "$temp_file"
    
    # Add everything after chat activity section (if it exists)
    sed -n '/## 🔄 Session Activity/,$p' "$DELTA_FILE" >> "$temp_file"
    
    # Replace original file
    mv "$temp_file" "$DELTA_FILE"
    
    # Clean up backup file after successful update
    rm -f "$DELTA_FILE.backup"
    
    log "${GREEN}✅ Updated existing delta file with latest git activity${NC}"
}

# Main execution
main() {
    log "${GREEN}🤖 Daily Session Summary Generator${NC}"
    log "📅 Date: $TARGET_DATE"
    
    # Check repository
    check_repo
    
    # Create summary directory if it doesn't exist
    mkdir -p "$SUMMARY_DIR"
    
    # Ensure monthly directory exists
    ensure_month_directory
    
    # Check if delta file already exists
    if [ -f "$DELTA_FILE" ]; then
        update_existing_summary
        return 0
    fi
    
    # Detect activity and create appropriate summary
    if detect_activity; then
        log "${GREEN}🎯 Development activity detected${NC}"
        create_active_summary
        log "${GREEN}✅ Summary created: $DELTA_FILE${NC}"
        # Show summary stats
        log "📊 Summary contains $(wc -l < "$DELTA_FILE") lines"
    else
        log "${YELLOW}😴 No development activity detected${NC}"
        # Heartbeat log for automation
        HEARTBEAT_LOG="$REPO_DIR/dev/logs/automation-heartbeat.log"
        mkdir -p "$REPO_DIR/dev/logs"
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] No development activity detected (heartbeat)" >> "$HEARTBEAT_LOG"
        log "${GREEN}✅ Heartbeat logged: $HEARTBEAT_LOG${NC}"
    fi
}

# Run main function
main "$@"
