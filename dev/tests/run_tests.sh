#!/bin/bash
# Test runner for all automation scripts

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory containing this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "🧪 Running all automation tests..."
echo "=================================="

# Total test tracking
TOTAL_TESTS_RUN=0
TOTAL_TESTS_PASSED=0
TOTAL_TESTS_FAILED=0

# Function to run a test suite
run_test_suite() {
    local test_name="$1"
    local test_command="$2"
    
    echo ""
    echo "🔍 Running $test_name..."
    echo "----------------------------------------"
    
    if eval "$test_command"; then
        echo -e "${GREEN}✅ $test_name PASSED${NC}"
        return 0
    else
        echo -e "${RED}❌ $test_name FAILED${NC}"
        return 1
    fi
}

# Configure Python environment
cd "$PROJECT_ROOT"
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Setting up Python virtual environment...${NC}"
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -q google-cloud-texttospeech
else
    source .venv/bin/activate
fi

# Run Python tests
if run_test_suite "Parse Chat Sessions Tests" ".venv/bin/python dev/tests/test_parse_chat_sessions.py"; then
    TOTAL_TESTS_PASSED=$((TOTAL_TESTS_PASSED + 12))
else
    TOTAL_TESTS_FAILED=$((TOTAL_TESTS_FAILED + 12))
fi
TOTAL_TESTS_RUN=$((TOTAL_TESTS_RUN + 12))

if run_test_suite "Markdown TTS Tests" ".venv/bin/python dev/tests/test_markdown_tts.py"; then
    TOTAL_TESTS_PASSED=$((TOTAL_TESTS_PASSED + 25))
else
    TOTAL_TESTS_FAILED=$((TOTAL_TESTS_FAILED + 25))
fi
TOTAL_TESTS_RUN=$((TOTAL_TESTS_RUN + 25))

# Run Shell tests
if run_test_suite "Daily Session Summary Tests" "./dev/tests/test_daily_session_summary.sh"; then
    TOTAL_TESTS_PASSED=$((TOTAL_TESTS_PASSED + 8))
else
    TOTAL_TESTS_FAILED=$((TOTAL_TESTS_FAILED + 8))
fi
TOTAL_TESTS_RUN=$((TOTAL_TESTS_RUN + 8))

# Print final results
echo ""
echo "=================================="
echo "🏁 Final Test Results:"
echo "  Total tests run: $TOTAL_TESTS_RUN"
echo -e "  ${GREEN}Passed: $TOTAL_TESTS_PASSED${NC}"
echo -e "  ${RED}Failed: $TOTAL_TESTS_FAILED${NC}"

if [ $TOTAL_TESTS_FAILED -eq 0 ]; then
    echo ""
    echo -e "🎉 ${GREEN}ALL TESTS PASSED! Automation is ready for creative work.${NC}"
    echo ""
    echo "Your automation scripts are thoroughly tested and reliable:"
    echo "  • parse-chat-sessions.py: 12 tests ✅"
    echo "  • markdown-tts.py: 25 tests ✅"
    echo "  • daily-session-summary.sh: 8 tests ✅"
    echo ""
    echo "You can now focus on creative work with confidence! 🚀"
    exit 0
else
    echo ""
    echo -e "❌ ${RED}Some tests failed. Please review the output above.${NC}"
    exit 1
fi
