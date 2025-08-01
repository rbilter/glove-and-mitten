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

    # Include sessions that have been active within the last 7 days
    # VS Code sessions are long-lived and don't have per-message timestamps
    session_timestamp = session_data.get('lastMessageDate', 0) or session_data.get('creationDate', 0)
    if target_date and session_timestamp:
        session_date = datetime.fromtimestamp(session_timestamp / 1000, tz=timezone.utc).date()
        days_since_activity = (target_date - session_date).days
        if days_since_activity > 7:  # Skip sessions older than 7 days
            return []

    conversations = []
    requests = session_data.get('requests', [])
    
    # Since VS Code sessions can span multiple days and we can't filter by actual message timestamps,
    # we'll take ALL conversations from sessions that have been active within the last 7 days.
    # This ensures we capture the complete daily activity.
    
    # No conversation limiting - capture all conversations from active sessions
    # The 7-day session filter above already handles excluding very old sessions
    
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


def analyze_conversations_for_structure(conversations):
    """Analyze conversations and extract structured insights for session sections."""
    if not conversations:
        return {
            'tasks_worked_on': [],
            'decisions_made': [],
            'problems_solved': [],
            'ideas_discussed': [],
            'for_next_session': [],
            'notes': []
        }
    
    # Combine all conversation content for analysis
    all_content = []
    for conv in conversations:
        all_content.append(f"User: {conv['user_message']}")
        if conv['copilot_response']:
            all_content.append(f"Assistant: {conv['copilot_response']}")
    
    full_text = '\n'.join(all_content)
    
    # Analyze content and categorize insights
    insights = {
        'tasks_worked_on': extract_tasks(full_text),
        'decisions_made': extract_decisions(full_text),
        'problems_solved': extract_problems_and_solutions(full_text),
        'ideas_discussed': extract_ideas(full_text),
        'for_next_session': extract_next_steps(full_text),
        'notes': extract_notable_context(full_text)
    }
    
    return insights


def extract_tasks(text):
    """Extract tasks and implementation work from conversation."""
    tasks = []
    # Look for implementation patterns with better context
    patterns = [
        r"(?:implement(?:ed|ing)?|creat(?:ed|ing)?|build(?:ing)?|develop(?:ed|ing)?)\s+([^.!?\n]{10,80})",
        r"(?:work(?:ed|ing)?|add(?:ed|ing)?|fix(?:ed|ing)?)\s+(?:on\s+)?([^.!?\n]{10,80})",
        r"(?:enhanc(?:ed|ing)?|updat(?:ed|ing)?|improv(?:ed|ing)?)\s+([^.!?\n]{10,80})",
        r"(?:set\s+up|configur(?:ed|ing)?|establish(?:ed|ing)?)\s+([^.!?\n]{10,80})"
    ]
    
    import re
    processed = set()  # Track processed tasks to avoid duplicates
    
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            task = match.group(1).strip()
            # Clean up the task text
            task = re.sub(r'\s+', ' ', task)  # Normalize whitespace
            task = task.rstrip('.,;:')  # Remove trailing punctuation
            
            # Skip if too short, too long, or already processed
            if 10 <= len(task) <= 80 and task.lower() not in processed:
                processed.add(task.lower())
                tasks.append(f"- {task}")
    
    return tasks[:5]  # Limit to top 5 tasks


def extract_decisions(text):
    """Extract key decisions made during the session."""
    decisions = []
    patterns = [
        r"(?:decided?|chose|went\s+with)\s+(?:to\s+)?([^.!?\n]{10,100})",
        r"(?:option|approach|choice)\s+\d*[:.]\s*([^.!?\n]{10,100})",
        r"(?:strategy|plan|direction)[:.]\s*([^.!?\n]{10,100})",
        r"(?:let's|we'll|we\s+should)\s+(?:use|go\s+with|implement)\s+([^.!?\n]{10,100})"
    ]
    
    import re
    processed = set()
    
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            decision = match.group(1).strip()
            # Clean up the decision text
            decision = re.sub(r'\s+', ' ', decision)
            decision = decision.rstrip('.,;:')
            
            if 10 <= len(decision) <= 100 and decision.lower() not in processed:
                processed.add(decision.lower())
                decisions.append(f"- {decision}")
    
    return decisions[:3]  # Limit to top 3 decisions


def extract_problems_and_solutions(text):
    """Extract problems encountered and their solutions."""
    problems = []
    patterns = [
        r"(?:issue|problem|error|bug)[:.]\s*([^.!?\n]{10,100})",
        r"(?:fixed|solved|resolved|addressed)\s+(?:the\s+)?([^.!?\n]{10,100})",
        r"(?:hanging|failing|not\s+working)[:.]\s*([^.!?\n]{10,100})",
        r"(?:challenge|difficulty|trouble)[:.]\s*([^.!?\n]{10,100})"
    ]
    
    import re
    processed = set()
    
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            problem = match.group(1).strip()
            # Clean up the problem text
            problem = re.sub(r'\s+', ' ', problem)
            problem = problem.rstrip('.,;:')
            
            if 10 <= len(problem) <= 100 and problem.lower() not in processed:
                processed.add(problem.lower())
                problems.append(f"- {problem}")
    
    return problems[:3]  # Limit to top 3 problems


def extract_ideas(text):
    """Extract ideas and concepts discussed."""
    ideas = []
    patterns = [
        r"(?:idea|concept|thought)[:.]\s*([^.!?\n]{10,120})",
        r"(?:approach|strategy|method)[:.]\s*([^.!?\n]{10,120})",
        r"(?:could|might|maybe)\s+(?:we\s+)?([^.!?\n]{10,120})",
        r"(?:consider|suggest|recommend)\s+([^.!?\n]{10,120})",
        r"(?:what\s+if|how\s+about)\s+([^.!?\n]{10,120})"
    ]
    
    import re
    processed = set()
    
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            idea = match.group(1).strip()
            # Clean up the idea text
            idea = re.sub(r'\s+', ' ', idea)
            idea = idea.rstrip('.,;:')
            
            if 10 <= len(idea) <= 120 and idea.lower() not in processed:
                processed.add(idea.lower())
                ideas.append(f"- {idea}")
    
    return ideas[:4]  # Limit to top 4 ideas


def extract_next_steps(text):
    """Extract next steps and action items."""
    next_steps = []
    patterns = [
        r"(?:next|later|continue)\s+(?:we\s+)?(?:should\s+|will\s+|need\s+to\s+)?([^.!?\n]{10,100})",
        r"(?:need\s+to|should|plan\s+to)\s+([^.!?\n]{10,100})",
        r"(?:todo|action\s+item)[:.]\s*([^.!?\n]{10,100})",
        r"(?:for\s+next\s+session|tomorrow|future)[:.]\s*([^.!?\n]{10,100})"
    ]
    
    import re
    processed = set()
    
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            step = match.group(1).strip()
            # Clean up the step text
            step = re.sub(r'\s+', ' ', step)
            step = step.rstrip('.,;:')
            
            if 10 <= len(step) <= 100 and step.lower() not in processed:
                processed.add(step.lower())
                next_steps.append(f"- {step}")
    
    return next_steps[:3]  # Limit to top 3 next steps


def extract_notable_context(text):
    """Extract notable context and observations."""
    notes = []
    
    # Look for specific technical patterns and key themes
    context_patterns = [
        (r"git\s+commit.*hang", "Git commit hanging issue identified and addressed"),
        (r"multi-?line.*(?:command|issue|problem)", "Multi-line command execution challenges discussed"),
        (r"automation.*(?:improve|implement|enhance)", "Automation improvements implemented"),
        (r"vs\s*code.*(?:chat|copilot|integration)", "VS Code/Copilot integration work"),
        (r"(?:folder|directory).*(?:structure|organization)", "Project structure and organization improvements"),
        (r"workflow.*(?:create|establish|document)", "Workflow documentation and processes established"),
        (r"(?:sync|backup).*(?:google\s*drive|git)", "Sync and backup processes implemented"),
        (r"(?:series\s*bible|character.*profile)", "Creative project development and character work")
    ]
    
    import re
    for pattern, note in context_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            notes.append(f"- {note}")
    
    # Add any specific insights from the conversation content
    if "parse-chat-sessions" in text.lower():
        notes.append("- Chat session parsing and integration developed")
    
    if "heartbeat" in text.lower() and "automation" in text.lower():
        notes.append("- Heartbeat logging for automation monitoring implemented")
    
    return notes[:4]  # Limit to top 4 notes


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
    parser.add_argument('--format', choices=['summary', 'json', 'insights'], default='summary', 
                       help='Output format: summary (raw chat), json (data), insights (structured analysis)')
    
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
    elif args.format == 'insights':
        insights = analyze_conversations_for_structure(conversations)
        print(json.dumps(insights, indent=2))
    else:
        print(format_conversations_for_summary(conversations))


if __name__ == '__main__':
    main()
