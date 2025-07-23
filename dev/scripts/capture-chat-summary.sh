#!/bin/bash
# Chat Summary Capture Script
# Prompts AI to create a chat summary for today's session

set -e

# Configuration
REPO_DIR="/home/rbilter/work/repos/glove-and-mitten"
LOGS_DIR="$REPO_DIR/dev/logs"
TODAY=$(date +%Y-%m-%d)
CHAT_SUMMARY_FILE="$LOGS_DIR/chat-summary-$TODAY.txt"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to log with timestamp
log() {
    echo -e "[$(date '+%H:%M:%S')] $1"
}

main() {
    log "${GREEN}🗨️  Chat Summary Capture${NC}"
    log "📅 Date: $TODAY"
    
    # Check if summary already exists
    if [ -f "$CHAT_SUMMARY_FILE" ]; then
        log "${YELLOW}⚠️  Chat summary already exists: $CHAT_SUMMARY_FILE${NC}"
        read -p "Overwrite existing summary? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log "${RED}❌ Cancelled${NC}"
            exit 0
        fi
    fi
    
    # Create logs directory if it doesn't exist
    mkdir -p "$LOGS_DIR"
    
    log "${GREEN}📝 Ready to capture chat summary${NC}"
    log "${YELLOW}💡 In VS Code, ask GitHub Copilot to:${NC}"
    echo "   'Create a summary of today's chat session and save it to $CHAT_SUMMARY_FILE'"
    echo ""
    log "${GREEN}✅ Once Copilot creates the summary, tonight's automation will pick it up${NC}"
    log "🕐 The daily summary script will incorporate this chat content automatically"
}

main "$@"
