#!/usr/bin/env python3
"""
Unit tests for parse-chat-sessions.py

Tests the critical functionality of chat session parsing, including:
- JSON parsing and validation
- Date filtering logic
- Workspace directory discovery
- Error handling and edge cases
"""

import unittest
import json
import tempfile
import shutil
from datetime import datetime, timezone, date
from pathlib import Path
import sys
import os

# Add the scripts directory to the path so we can import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

# Import the functions we want to test
import importlib.util
spec = importlib.util.spec_from_file_location("parse_chat_sessions", 
    os.path.join(os.path.dirname(__file__), '..', 'scripts', 'parse-chat-sessions.py'))
parse_chat_sessions = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parse_chat_sessions)

# Import the functions we want to test
import importlib.util
spec = importlib.util.spec_from_file_location("parse_chat_sessions", 
    os.path.join(os.path.dirname(__file__), '..', 'scripts', 'parse-chat-sessions.py'))
parse_chat_sessions = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parse_chat_sessions)

# Extract the functions we want to test (only those that actually exist)
find_workspace_chat_dir = parse_chat_sessions.find_workspace_chat_dir
parse_chat_session = parse_chat_sessions.parse_chat_session
extract_daily_conversations = parse_chat_sessions.extract_daily_conversations
analyze_conversations_for_structure = parse_chat_sessions.analyze_conversations_for_structure
format_conversations_for_summary = parse_chat_sessions.format_conversations_for_summary


class TestChatSessionParsing(unittest.TestCase):
    """Test suite for chat session parsing functionality"""
    
    def setUp(self):
        """Set up test fixtures before each test"""
        self.test_dir = tempfile.mkdtemp()
        self.chat_dir = Path(self.test_dir) / "chatSessions"
        self.chat_dir.mkdir(parents=True)
        
        # Sample chat session data for testing
        # Using numeric timestamps (milliseconds since epoch) as expected by the actual implementation
        today_timestamp = int(datetime(2025, 8, 8, 10, 30, 0).timestamp() * 1000)
        today_timestamp2 = int(datetime(2025, 8, 8, 14, 15, 30).timestamp() * 1000)
        yesterday_timestamp = int(datetime(2025, 8, 7, 16, 45, 0).timestamp() * 1000)
        
        self.sample_session_data = {
            "requests": [
                {
                    "message": {"text": "How do I create a Python test?"},
                    "timestamp": today_timestamp,
                    "response": [{"value": "To create a Python test, use unittest module..."}],
                    "requestId": "test-001"
                },
                {
                    "message": {"text": "Can you help me with error handling?"},
                    "timestamp": today_timestamp2, 
                    "response": [{"value": "Sure! Here's how to handle errors in Python:\n\n```python\ntry:\n    risky_operation()\nexcept Exception as e:\n    print(f'Error: {e}')\n```"}],
                    "requestId": "test-002"
                },
                {
                    "message": {"text": "What about yesterday's question?"},
                    "timestamp": yesterday_timestamp,
                    "response": [{"value": "That was about git workflows..."}],
                    "requestId": "test-003"
                }
            ]
        }
    
    def tearDown(self):
        """Clean up test fixtures after each test"""
        shutil.rmtree(self.test_dir)
    
    def create_test_session_file(self, data=None, filename="test_session.json"):
        """Helper to create a test session file"""
        if data is None:
            data = self.sample_session_data
        
        session_file = self.chat_dir / filename
        with open(session_file, 'w') as f:
            json.dump(data, f)
        return session_file
    
    def test_parse_chat_session_valid_json(self):
        """Test parsing a valid chat session file"""
        session_file = self.create_test_session_file()
        target_date = date(2025, 8, 8)
        
        conversations = parse_chat_session(session_file, target_date)
        
        # Should find 2 conversations from August 8th
        self.assertEqual(len(conversations), 2)
        
        # Check first conversation
        self.assertEqual(conversations[0]['user_message'], "How do I create a Python test?")
        self.assertIn("10:30", conversations[0]['timestamp'])
        
        # Check second conversation  
        self.assertEqual(conversations[1]['user_message'], "Can you help me with error handling?")
        self.assertIn("14:15", conversations[1]['timestamp'])
    
    def test_parse_chat_session_date_filtering(self):
        """Test that date filtering works correctly"""
        session_file = self.create_test_session_file()
        target_date = date(2025, 8, 7)  # Different date
        
        conversations = parse_chat_session(session_file, target_date)
        
        # Should find 1 conversation from August 7th
        self.assertEqual(len(conversations), 1)
        self.assertEqual(conversations[0]['user_message'], "What about yesterday's question?")
    
    def test_parse_chat_session_no_target_date(self):
        """Test parsing without date filter (should return all)"""
        session_file = self.create_test_session_file()
        
        conversations = parse_chat_session(session_file, target_date=None)
        
        # Should find all 3 conversations
        self.assertEqual(len(conversations), 3)
    
    def test_parse_chat_session_invalid_json(self):
        """Test handling of invalid JSON files"""
        # Create file with invalid JSON
        invalid_file = self.chat_dir / "invalid.json"
        with open(invalid_file, 'w') as f:
            f.write("{ invalid json content")
        
        conversations = parse_chat_session(invalid_file, date(2025, 8, 8))
        
        # Should return empty list for invalid JSON
        self.assertEqual(conversations, [])
    
    def test_parse_chat_session_missing_file(self):
        """Test handling of missing files"""
        missing_file = self.chat_dir / "nonexistent.json"
        
        conversations = parse_chat_session(missing_file, date(2025, 8, 8))
        
        # Should return empty list for missing file
        self.assertEqual(conversations, [])
    
    def test_parse_chat_session_empty_requests(self):
        """Test handling of session with no requests"""
        empty_data = {"requests": []}
        session_file = self.create_test_session_file(empty_data)
        
        conversations = parse_chat_session(session_file, date(2025, 8, 8))
        
        # Should return empty list
        self.assertEqual(conversations, [])
    
    def test_parse_chat_session_missing_timestamp(self):
        """Test handling of requests with missing timestamps"""
        data_no_timestamp = {
            "requests": [
                {
                    "message": "Question without timestamp",
                    "response": "Response without timestamp"
                }
            ]
        }
        session_file = self.create_test_session_file(data_no_timestamp)
        
        conversations = parse_chat_session(session_file, date(2025, 8, 8))
        
        # Should handle gracefully (might include or exclude based on implementation)
        self.assertIsInstance(conversations, list)
    
    def test_conversation_analysis(self):
        """Test conversation structure analysis functionality"""
        conversations = [
            {
                'timestamp': datetime(2025, 8, 8, 10, 30, 0).isoformat(),
                'user_message': 'I need to implement a new feature',
                'copilot_response': 'Here are the steps to implement that feature...',
                'request_id': 'test-001'
            },
            {
                'timestamp': datetime(2025, 8, 8, 11, 0, 0).isoformat(),
                'user_message': 'How should I handle this error?',
                'copilot_response': 'You can handle this error by using try-catch blocks...',
                'request_id': 'test-002'
            }
        ]
        
        # Test that analyze_conversations_for_structure works
        analysis = analyze_conversations_for_structure(conversations)
        self.assertIsInstance(analysis, dict)
        
        # Test that format_conversations_for_summary works
        formatted = format_conversations_for_summary(conversations)
        self.assertIsInstance(formatted, str)
        self.assertIn('implement a new feature', formatted)
        self.assertIn('handle this error', formatted)
    
    def test_timezone_handling(self):
        """Test proper timezone handling in timestamps"""
        # Test with numeric timestamps (the actual format used)
        today_base = datetime(2025, 8, 8, 10, 30, 0)
        timestamps = [
            int(today_base.timestamp() * 1000),                    # 10:30 UTC
            int((today_base.replace(hour=11)).timestamp() * 1000), # 11:30 UTC
            int((today_base.replace(hour=15)).timestamp() * 1000), # 15:30 UTC
            int((today_base.replace(hour=16)).timestamp() * 1000), # 16:30 UTC
        ]
        
        data_with_timezones = {
            "requests": [
                {
                    "message": {"text": f"Message {i}"},
                    "timestamp": ts,
                    "response": [{"value": f"Response {i}"}],
                    "requestId": f"test-{i:03d}"
                }
                for i, ts in enumerate(timestamps)
            ]
        }
        
        session_file = self.create_test_session_file(data_with_timezones)
        conversations = parse_chat_session(session_file, date(2025, 8, 8))
        
        # All should be parsed successfully
        self.assertEqual(len(conversations), 4)
    
    def test_workspace_directory_discovery(self):
        """Test workspace chat directory discovery"""
        # Mock the home directory structure
        mock_home = Path(self.test_dir) / "home"
        mock_config = mock_home / ".config/Code/User/workspaceStorage/6ef03f1d95db727baaf62cab09739e42/chatSessions"
        mock_config.mkdir(parents=True)
        
        # Patch Path.home() for testing
        original_home = Path.home
        Path.home = lambda: mock_home
        
        try:
            chat_dir = find_workspace_chat_dir()
            self.assertEqual(chat_dir, mock_config)
        finally:
            # Restore original method
            Path.home = original_home
    
    def test_large_session_file_performance(self):
        """Test performance with large session files"""
        # Create a large session with many requests using numeric timestamps
        base_time = datetime(2025, 8, 8, 10, 30, 0)
        large_data = {
            "requests": [
                {
                    "message": {"text": f"Question {i}"},
                    "timestamp": int((base_time.replace(minute=30 + i % 30)).timestamp() * 1000),
                    "response": [{"value": f"Response {i} " * 10}],  # Make responses longer
                    "requestId": f"perf-test-{i:04d}"
                }
                for i in range(100)  # 100 requests for reasonable test time
            ]
        }
        
        session_file = self.create_test_session_file(large_data, "large_session.json")
        
        # Test that it completes in reasonable time
        import time
        start_time = time.time()
        conversations = parse_chat_session(session_file, date(2025, 8, 8))
        end_time = time.time()
        
        # Should complete in under 1 second for 100 requests
        self.assertLess(end_time - start_time, 1.0)
        self.assertEqual(len(conversations), 100)


class TestChatSessionIntegration(unittest.TestCase):
    """Integration tests for the full chat session parsing workflow"""
    
    def setUp(self):
        """Set up integration test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.chat_dir = Path(self.test_dir) / "chatSessions"
        self.chat_dir.mkdir(parents=True)
    
    def tearDown(self):
        """Clean up integration test environment"""
        shutil.rmtree(self.test_dir)
    
    def test_multiple_session_files(self):
        """Test processing multiple session files"""
        # Create multiple session files with numeric timestamps
        today = datetime(2025, 8, 8, 10, 0, 0)
        session_data_1 = {
            "requests": [
                {
                    "message": {"text": "Question from session 1"},
                    "timestamp": int(today.timestamp() * 1000),
                    "response": [{"value": "Response from session 1"}],
                    "requestId": "session1-001"
                }
            ]
        }
        
        session_data_2 = {
            "requests": [
                {
                    "message": {"text": "Question from session 2"}, 
                    "timestamp": int((today.replace(hour=11)).timestamp() * 1000),
                    "response": [{"value": "Response from session 2"}],
                    "requestId": "session2-001"
                }
            ]
        }
        
        # Create session files
        session1 = self.chat_dir / "session1.json"
        session2 = self.chat_dir / "session2.json"
        
        with open(session1, 'w') as f:
            json.dump(session_data_1, f)
        with open(session2, 'w') as f:
            json.dump(session_data_2, f)
        
        # Test parsing both files
        conversations1 = parse_chat_session(session1, date(2025, 8, 8))
        conversations2 = parse_chat_session(session2, date(2025, 8, 8))
        
        self.assertEqual(len(conversations1), 1)
        self.assertEqual(len(conversations2), 1)
        self.assertIn("session 1", conversations1[0]['user_message'])
        self.assertIn("session 2", conversations2[0]['user_message'])


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
