#!/bin/bash
# Test runner for the parse-chat-sessions.py module

echo "🧪 Running parse-chat-sessions.py unit tests..."
echo "=================================================="

cd "$(dirname "$0")/../.."

# Ensure we're in the right directory
if [ ! -f "dev/scripts/parse-chat-sessions.py" ]; then
    echo "❌ Error: parse-chat-sessions.py not found. Run from project root."
    exit 1
fi

# Run the tests
python3 dev/tests/test_parse_chat_sessions.py -v

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All tests passed! The parse-chat-sessions.py module is working correctly."
    echo ""
    echo "Tested functionality:"
    echo "  • JSON parsing and validation"
    echo "  • Date filtering logic" 
    echo "  • Workspace directory discovery"
    echo "  • Error handling (invalid JSON, missing files)"
    echo "  • Timestamp conversion and timezone handling"
    echo "  • Performance with large session files"
    echo "  • Integration across multiple session files"
    echo ""
else
    echo ""
    echo "❌ Some tests failed. Check the output above for details."
    echo ""
    exit 1
fi
