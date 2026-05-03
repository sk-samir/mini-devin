#!/usr/bin/env python
"""
Log viewer for Mini Devin application logs.
Usage: python view_logs.py [--tail] [--filter FILTER] [--level LEVEL]
"""

import argparse
import json
import os
from pathlib import Path
from datetime import datetime
import time

def parse_log_line(line):
    """Parse a JSON log line."""
    try:
        return json.loads(line.strip())
    except json.JSONDecodeError:
        return None

def format_log_entry(entry):
    """Format a log entry for display."""
    timestamp = entry.get('timestamp', 'Unknown')
    level = entry.get('level', 'UNKNOWN')
    logger = entry.get('logger', 'unknown')
    message = entry.get('message', '')

    # Color coding for levels
    colors = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
    }
    reset = '\033[0m'
    color = colors.get(level, reset)

    return f"{color}{timestamp} [{level}] {logger}: {message}{reset}"

def view_logs(log_file=None, tail=False, filter_text=None, level=None, follow=False):
    """View logs from the specified file or all log files."""

    logs_dir = Path("logs")
    if not logs_dir.exists():
        print("❌ Logs directory not found. Run the application first to generate logs.")
        return

    if log_file:
        log_files = [logs_dir / log_file]
    else:
        # Get all log files
        log_files = list(logs_dir.glob("*.log"))
        log_files.sort()

    if not log_files:
        print("❌ No log files found.")
        return

    print(f"📋 Viewing logs from: {', '.join(str(f.name) for f in log_files)}")
    print("=" * 80)

    try:
        while True:
            lines_shown = 0

            for log_path in log_files:
                if not log_path.exists():
                    continue

                with open(log_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                    if tail:
                        lines = lines[-50:]  # Show last 50 lines

                    for line in lines:
                        entry = parse_log_line(line)
                        if not entry:
                            continue

                        # Apply filters
                        if filter_text and filter_text.lower() not in json.dumps(entry).lower():
                            continue

                        if level and entry.get('level') != level.upper():
                            continue

                        print(format_log_entry(entry))
                        lines_shown += 1

            if not follow:
                break

            if follow:
                time.sleep(1)
                print("\n" + "=" * 80 + f"\nUpdated at {datetime.now().strftime('%H:%M:%S')}\n" + "=" * 80)

    except KeyboardInterrupt:
        print("\n✅ Log viewing stopped.")
    except Exception as e:
        print(f"❌ Error reading logs: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="View Mini Devin application logs")
    parser.add_argument('--file', '-f', help='Specific log file to view (e.g., api.log, agent.log)')
    parser.add_argument('--tail', '-t', action='store_true', help='Show only the last 50 lines')
    parser.add_argument('--filter', help='Filter logs containing this text')
    parser.add_argument('--level', '-l', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                       help='Show only logs of this level')
    parser.add_argument('--follow', action='store_true', help='Follow log file (like tail -f)')

    args = parser.parse_args()

    view_logs(
        log_file=args.file,
        tail=args.tail,
        filter_text=args.filter,
        level=args.level,
        follow=args.follow
    )

if __name__ == "__main__":
    main()