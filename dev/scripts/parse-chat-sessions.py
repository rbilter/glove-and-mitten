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
    # Use the correct workspace for this project
    correct_path = Path.home() / ".config/Code/User/workspaceStorage/6ef03f1d95db727baaf62cab09739e42/chatSessions"
    if correct_path.exists():
        return correct_path
    
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

    conversations = []
    requests = session_data.get('requests', [])
    
    # VS Code now provides individual timestamps for each request!
    # Filter conversations by their actual individual timestamps
    
    for i, request in enumerate(requests):
        # Use the individual request timestamp (the key discovery!)
        individual_timestamp = request.get('timestamp', 0)
        
        if individual_timestamp:
            # Convert individual timestamp to local timezone for filtering and display
            msg_date = datetime.fromtimestamp(individual_timestamp / 1000)
            request_date = msg_date.date()
            
            # Filter by target date if specified
            if target_date and request_date != target_date:
                continue  # Skip this conversation, it's not from the target date
        else:
            # Fallback: if no individual timestamp, skip this request
            continue
        
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
    # Look for implementation patterns with complete sentences or meaningful phrases
    patterns = [
        r"(?:implement(?:ed|ing)?|creat(?:ed|ing)?|build(?:ing|t)?|develop(?:ed|ing)?)\s+([a-zA-Z][^.!?\n]{20,120}(?:[.!?]|$))",
        r"(?:work(?:ed|ing)?|add(?:ed|ing)?|fix(?:ed|ing)?)\s+(?:on\s+)?([a-zA-Z][^.!?\n]{20,120}(?:[.!?]|$))",
        r"(?:enhanc(?:ed|ing)?|updat(?:ed|ing)?|improv(?:ed|ing)?)\s+([a-zA-Z][^.!?\n]{20,120}(?:[.!?]|$))",
        r"(?:set\s+up|configur(?:ed|ing)?|establish(?:ed|ing)?)\s+([a-zA-Z][^.!?\n]{20,120}(?:[.!?]|$))"
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
            
            # Skip if too short, contains markdown artifacts, or already processed
            if (20 <= len(task) <= 120 and 
                task.lower() not in processed and
                not any(artifact in task for artifact in ['```', '##', '**', '- ['])):
                processed.add(task.lower())
                tasks.append(f"- {task}")
    
    return tasks[:5]  # Limit to top 5 tasks


def extract_decisions(text):
    """Extract key decisions made during the session."""
    decisions = []
    patterns = [
        r"(?:decided?|chose|went\s+with)\s+(?:to\s+)?([a-zA-Z][^.!?\n]{20,150}(?:[.!?]|$))",
        r"(?:option|approach|choice)\s+\d*[:.]\s*([a-zA-Z][^.!?\n]{20,150}(?:[.!?]|$))",
        r"(?:strategy|plan|direction)[:.]\s*([a-zA-Z][^.!?\n]{20,150}(?:[.!?]|$))",
        r"(?:let's|we'll|we\s+should)\s+(?:use|go\s+with|implement)\s+([a-zA-Z][^.!?\n]{20,150}(?:[.!?]|$))"
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
            
            if (20 <= len(decision) <= 150 and 
                decision.lower() not in processed and
                not any(artifact in decision for artifact in ['```', '##', '**', '- ['])):
                processed.add(decision.lower())
                decisions.append(f"- {decision}")
    
    return decisions[:3]  # Limit to top 3 decisions


def extract_problems_and_solutions(text):
    """Extract problems encountered and their solutions."""
    problems = []
    patterns = [
        r"(?:issue|problem|error|bug)[:.]\s*([^.!?\n]{15,150}[.!?]?)",
        r"(?:fixed|solved|resolved|addressed)\s+(?:the\s+)?([^.!?\n]{15,150}[.!?]?)",
        r"(?:hanging|failing|not\s+working)[:.]\s*([^.!?\n]{15,150}[.!?]?)",
        r"(?:challenge|difficulty|trouble)[:.]\s*([^.!?\n]{15,150}[.!?]?)"
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
            
            if 15 <= len(problem) <= 150 and problem.lower() not in processed:
                processed.add(problem.lower())
                problems.append(f"- {problem}")
    
    return problems[:3]  # Limit to top 3 problems


def extract_ideas(text):
    """Extract ideas and concepts discussed."""
    ideas = []
    patterns = [
        r"(?:idea|concept|thought)[:.]\s*([^.!?\n]{15,180}[.!?]?)",
        r"(?:approach|strategy|method)[:.]\s*([^.!?\n]{15,180}[.!?]?)",
        r"(?:could|might|maybe)\s+(?:we\s+)?([^.!?\n]{15,180}[.!?]?)",
        r"(?:consider|suggest|recommend)\s+([^.!?\n]{15,180}[.!?]?)",
        r"(?:what\s+if|how\s+about)\s+([^.!?\n]{15,180}[.!?]?)"
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
            
            if 15 <= len(idea) <= 180 and idea.lower() not in processed:
                processed.add(idea.lower())
                ideas.append(f"- {idea}")
    
    return ideas[:4]  # Limit to top 4 ideas


def extract_next_steps(text):
    """Extract next steps and action items."""
    next_steps = []
    patterns = [
        r"(?:next|later|continue)\s+(?:we\s+)?(?:should\s+|will\s+|need\s+to\s+)?([^.!?\n]{15,150}[.!?]?)",
        r"(?:need\s+to|should|plan\s+to)\s+([^.!?\n]{15,150}[.!?]?)",
        r"(?:todo|action\s+item)[:.]\s*([^.!?\n]{15,150}[.!?]?)",
        r"(?:for\s+next\s+session|tomorrow|future)[:.]\s*([^.!?\n]{15,150}[.!?]?)"
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
            
            if 15 <= len(step) <= 150 and step.lower() not in processed:
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
        
        # Truncate very long messages at word boundaries
        user_msg = conv['user_message']
        if len(user_msg) > 2000:
            # Find the last word boundary before 2000 chars
            truncate_pos = user_msg.rfind(' ', 0, 2000)
            if truncate_pos > 1500:  # Make sure we don't truncate too early
                user_msg = user_msg[:truncate_pos] + "..."
            else:
                user_msg = user_msg[:2000] + "..."
        
        # Use proper markdown formatting instead of blockquotes
        formatted.append(f"{user_msg}")
        formatted.append("")
        
        if conv['copilot_response']:
            formatted.append("**Copilot:**")
            copilot_msg = conv['copilot_response']
            if len(copilot_msg) > 2000:
                # Find the last word boundary before 2000 chars
                truncate_pos = copilot_msg.rfind(' ', 0, 2000)
                if truncate_pos > 1500:  # Make sure we don't truncate too early
                    copilot_msg = copilot_msg[:truncate_pos] + "..."
                else:
                    copilot_msg = copilot_msg[:2000] + "..."
            formatted.append(f"{copilot_msg}")
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
