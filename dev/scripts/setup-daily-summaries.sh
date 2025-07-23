#!/bin/bash
# Setup script for automated daily session summaries

set -e

SCRIPT_DIR="/home/rbilter/work/repos/glove-and-mitten/dev/scripts"
SUMMARY_SCRIPT="$SCRIPT_DIR/daily-session-summary.sh"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log() {
    echo -e "[$(date '+%H:%M:%S')] $1"
}

# Function to setup cron job
setup_cron() {
    log "${GREEN}🕐 Setting up daily cron job...${NC}"
    
    # Check if cron job already exists
    if crontab -l 2>/dev/null | grep -q "daily-session-summary.sh"; then
        log "${YELLOW}⚠️  Cron job already exists${NC}"
        log "Current cron jobs:"
        crontab -l | grep "daily-session-summary.sh"
        echo ""
        read -p "Replace existing cron job? (y/N): " replace
        if [[ ! "$replace" =~ ^[Yy]$ ]]; then
            log "❌ Skipping cron setup"
            return 1
        fi
        
        # Remove existing cron job
        crontab -l | grep -v "daily-session-summary.sh" | crontab -
        log "${GREEN}✅ Removed existing cron job${NC}"
    fi
    
    # Add new cron job (runs at 11:50 PM daily)
    (crontab -l 2>/dev/null; echo "50 23 * * * $SUMMARY_SCRIPT >> /tmp/daily-session-summary.log 2>&1") | crontab -
    
    log "${GREEN}✅ Cron job installed successfully${NC}"
    log "📅 Will run daily at 11:50 PM"
    log "📋 Logs will be written to /tmp/daily-session-summary.log"
}

# Function to test the script
test_script() {
    log "${GREEN}🧪 Testing daily session summary script...${NC}"
    
    if [ ! -f "$SUMMARY_SCRIPT" ]; then
        log "${RED}❌ Script not found: $SUMMARY_SCRIPT${NC}"
        return 1
    fi
    
    if [ ! -x "$SUMMARY_SCRIPT" ]; then
        log "${RED}❌ Script not executable: $SUMMARY_SCRIPT${NC}"
        return 1
    fi
    
    log "🚀 Running test..."
    "$SUMMARY_SCRIPT"
    
    log "${GREEN}✅ Script test completed${NC}"
}

# Function to show current setup
show_status() {
    log "${GREEN}📊 Current Setup Status${NC}"
    echo ""
    
    # Check script exists
    if [ -f "$SUMMARY_SCRIPT" ]; then
        log "✅ Script exists: $SUMMARY_SCRIPT"
        if [ -x "$SUMMARY_SCRIPT" ]; then
            log "✅ Script is executable"
        else
            log "❌ Script is not executable"
        fi
    else
        log "❌ Script not found: $SUMMARY_SCRIPT"
    fi
    
    # Check cron job
    if crontab -l 2>/dev/null | grep -q "daily-session-summary.sh"; then
        log "✅ Cron job installed:"
        crontab -l | grep "daily-session-summary.sh" | sed 's/^/    /'
    else
        log "❌ No cron job found"
    fi
    
    # Check recent summaries
    local summary_dir="/home/rbilter/work/repos/glove-and-mitten/dev/logs/conversation-summaries"
    if [ -d "$summary_dir" ]; then
        local recent_files
        recent_files=$(ls -t "$summary_dir"/*.md 2>/dev/null | head -3)
        if [ -n "$recent_files" ]; then
            log "📁 Recent summary files:"
            echo "$recent_files" | sed 's/^/    /'
        else
            log "📁 No summary files found"
        fi
    else
        log "📁 Summary directory not found"
    fi
}

# Function to remove automation
remove_automation() {
    log "${YELLOW}🗑️  Removing automation...${NC}"
    
    # Remove cron job
    if crontab -l 2>/dev/null | grep -q "daily-session-summary.sh"; then
        crontab -l | grep -v "daily-session-summary.sh" | crontab -
        log "✅ Cron job removed"
    else
        log "ℹ️  No cron job found to remove"
    fi
    
    log "${GREEN}✅ Automation removed${NC}"
}

# Main menu
main() {
    log "${GREEN}🤖 Daily Session Summary Setup${NC}"
    echo ""
    
    case "${1:-menu}" in
        "install")
            setup_cron
            ;;
        "test")
            test_script
            ;;
        "status")
            show_status
            ;;
        "remove")
            remove_automation
            ;;
        "menu"|*)
            echo "Available commands:"
            echo "  install - Setup automated daily summaries"
            echo "  test    - Test the summary script"
            echo "  status  - Show current setup status"
            echo "  remove  - Remove automation"
            echo ""
            echo "Usage: $0 [install|test|status|remove]"
            ;;
    esac
}

main "$@"
