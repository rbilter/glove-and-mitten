#!/usr/bin/env python3
"""
Parse VS Code GitHub Copilot Chat Sessions for Daily Summaries

This script extracts chat conversations from VS Code's stored chat sessions
and formats them for inclusion in daily session summaries.
"""

import json
import sys
import os
from datetime import datetime, timezone
from pathlib import Path
import argparse


def find_workspace_chat_dir():
    """Find the current workspace's chat session directory."""
    vscode_storage = Path.home() / ".config/Code/User/workspaceStorage"
    
    if not vscode_storage.exists():
        return None
    
    # Look for workspace.json files that mention this project
    current_dir = Path.cwd()
    project_name = current_dir.name
    
    for workspace_dir in vscode_storage.iterdir():
        if workspace_dir.is_dir():
            workspace_json = workspace_dir / "workspace.json"
            if workspace_json.exists():
                try:
                    with open(workspace_json) as f:
                        content = f.read()
                        if project_name in content or str(current_dir) in content:
                            chat_sessions_dir = workspace_dir / "chatSessions"
                            if chat_sessions_dir.exists():
                                return chat_sessions_dir
                except (json.JSONDecodeError, IOError):
                    continue
    
    return None


def parse_chat_session(session_file, target_date=None):
    """
    Parse a single chat session file and extract conversations from target date.
    
    Args:
        session_file: Path to the JSON session file
        target_date: datetime.date object for filtering (None for all)
    
    Returns:
        List of conversation entries from the target date
    """
    try:
        with open(session_file, 'r') as f:
            session_data = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading {session_file}: {e}", file=sys.stderr)
        return []

    # Check if this session matches the target date based on session timestamps
    session_timestamp = session_data.get('lastMessageDate', 0) or session_data.get('creationDate', 0)
    if target_date and session_timestamp:
        session_date = datetime.fromtimestamp(session_timestamp / 1000, tz=timezone.utc).date()
        if session_date != target_date:
            return []  # Skip this session entirely if it doesn't match the date

    conversations = []
    requests = session_data.get('requests', [])
    
    # Use session timestamp as a base for individual messages
    base_timestamp = session_timestamp or datetime.now(timezone.utc).timestamp() * 1000
    
    for i, request in enumerate(requests):
        # Use session timestamp + offset for individual messages
        msg_timestamp = base_timestamp + (i * 1000)  # Add 1 second per message
        msg_date = datetime.fromtimestamp(msg_timestamp / 1000, tz=timezone.utc)
        
        # Extract user message
        message = request.get('message', {})
        user_text = message.get('text', '').strip()
        
        # Extract response
        response = request.get('response', [])
        response_text = ""
        if response and isinstance(response, list) and len(response) > 0:
            # Response is a list of response parts
            response_parts = []
            for part in response:
                if isinstance(part, dict) and 'value' in part:
                    value = part['value']
                    if isinstance(value, str):
                        response_parts.append(value.strip())
                    else:
                        response_parts.append(str(value))
            response_text = ' '.join(response_parts).strip()
        elif isinstance(response, dict) and 'value' in response:
            # Fallback for different response structure
            response_text = str(response['value']).strip()
        
        if user_text:  # Only include if there's actual user content
                conversations.append({
                    'timestamp': msg_date.isoformat(),
                    'user_message': user_text,
                    'copilot_response': response_text,
                    'request_id': request.get('requestId', '')
                })
    
    return conversations


def extract_daily_conversations(target_date=None):
    """
    Extract all conversations from the target date.
    
    Args:
        target_date: datetime.date object (defaults to today)
    
    Returns:
        List of all conversations from target date
    """
    if target_date is None:
        target_date = datetime.now().date()
    
    chat_dir = find_workspace_chat_dir()
    if not chat_dir:
        print("No chat sessions directory found for current workspace", file=sys.stderr)
        return []
    
    all_conversations = []
    
    # Process all session files
    for session_file in chat_dir.glob("*.json"):
        conversations = parse_chat_session(session_file, target_date)
        all_conversations.extend(conversations)
    
    # Sort by timestamp
    all_conversations.sort(key=lambda x: x['timestamp'])
    
    return all_conversations


def format_conversations_for_summary(conversations):
    """Format conversations for inclusion in daily summary."""
    if not conversations:
        return "No chat conversations found for this date."
    
    formatted = []
    formatted.append(f"## 💬 Chat Conversations ({len(conversations)} exchanges)")
    formatted.append("")
    
    for i, conv in enumerate(conversations, 1):
        # Parse timestamp for readable format
        timestamp = datetime.fromisoformat(conv['timestamp'])
        time_str = timestamp.strftime("%H:%M")
        
        formatted.append(f"### {i}. Chat at {time_str}")
        formatted.append("")
        formatted.append("**User:**")
        
        # Truncate very long messages
        user_msg = conv['user_message']
        if len(user_msg) > 500:
            user_msg = user_msg[:500] + "..."
        formatted.append(f"> {user_msg}")
        formatted.append("")
        
        if conv['copilot_response']:
            formatted.append("**Copilot:**")
            copilot_msg = conv['copilot_response']
            if len(copilot_msg) > 500:
                copilot_msg = copilot_msg[:500] + "..."
            formatted.append(f"> {copilot_msg}")
            formatted.append("")
        
        formatted.append("---")
        formatted.append("")
    
    return '\n'.join(formatted)


def main():
    parser = argparse.ArgumentParser(description='Parse VS Code chat sessions for daily summaries')
    parser.add_argument('--date', type=str, help='Target date (YYYY-MM-DD), defaults to today')
    parser.add_argument('--format', choices=['summary', 'json'], default='summary', 
                       help='Output format')
    
    args = parser.parse_args()
    
    # Parse target date
    target_date = None
    if args.date:
        try:
            target_date = datetime.strptime(args.date, '%Y-%m-%d').date()
        except ValueError:
            print(f"Invalid date format: {args.date}. Use YYYY-MM-DD", file=sys.stderr)
            sys.exit(1)
    
    # Extract conversations
    conversations = extract_daily_conversations(target_date)
    
    # Output in requested format
    if args.format == 'json':
        print(json.dumps(conversations, indent=2))
    else:
        print(format_conversations_for_summary(conversations))


if __name__ == '__main__':
    main()
