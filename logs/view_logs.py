#!/usr/bin/env python3
"""
Log Viewer - CLI tool for viewing application logs

Usage:
    python logs/view_logs.py                    # Last 50 lines
    python logs/view_logs.py --lines 100        # Last 100 lines
    python logs/view_logs.py --level ERROR      # Only errors
    python logs/view_logs.py --request-id abc   # Filter by request ID
    python logs/view_logs.py --follow           # Follow mode (like tail -f)
    python logs/view_logs.py --search "keyword" # Search in messages
"""

import argparse
import json
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
LOG_DIR = SCRIPT_DIR
LOG_FILE = LOG_DIR / "application.log"
JSON_LOG_FILE = LOG_DIR / "application.jsonl"

# ANSI color codes
COLORS = {
    'ERROR': '\033[91m',     # Red
    'WARNING': '\033[93m',   # Yellow
    'INFO': '\033[92m',      # Green
    'DEBUG': '\033[94m',     # Blue
    'RESET': '\033[0m',
    'BOLD': '\033[1m',
    'DIM': '\033[2m',
}


def colorize(text: str, level: str) -> str:
    """Apply color based on log level"""
    color = COLORS.get(level, '')
    return f"{color}{text}{COLORS['RESET']}"


def view_text_logs(lines: int, level: str, request_id: str, search: str, follow: bool):
    """View traditional text log file"""
    if not LOG_FILE.exists():
        print(f"Log file not found: {LOG_FILE}")
        return

    def print_filtered_lines(content: list):
        for line in content:
            # Apply filters
            if level and f"| {level}" not in line.upper():
                continue
            if request_id and request_id not in line:
                continue
            if search and search.lower() not in line.lower():
                continue

            # Colorize output
            for lvl in ['ERROR', 'WARNING', 'INFO', 'DEBUG']:
                if f"| {lvl}" in line:
                    line = colorize(line.rstrip(), lvl)
                    break

            print(line)

    if follow:
        # Follow mode
        print(f"Following {LOG_FILE} (Ctrl+C to stop)...")
        try:
            with open(LOG_FILE, 'r') as f:
                # Go to end of file
                f.seek(0, 2)
                while True:
                    line = f.readline()
                    if line:
                        print_filtered_lines([line])
                    else:
                        time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nStopped following.")
    else:
        # Read last N lines
        with open(LOG_FILE, 'r') as f:
            all_lines = f.readlines()
            print_filtered_lines(all_lines[-lines:])


def view_json_logs(lines: int, level: str, request_id: str, search: str, follow: bool):
    """View JSON log file with structured output"""
    if not JSON_LOG_FILE.exists():
        print(f"JSON log file not found: {JSON_LOG_FILE}")
        return

    def format_entry(entry: dict) -> str:
        """Format a JSON log entry for display"""
        ts = entry.get('ts', '')[:19]  # Trim to seconds
        lvl = entry.get('level', 'INFO')
        module = entry.get('module', 'MAIN')
        req_id = entry.get('request_id', '----')[:8]
        msg = entry.get('msg', '')

        # Add duration if present
        duration = entry.get('duration_ms')
        if duration:
            msg += f" [{duration:.0f}ms]"

        line = f"{ts} | {lvl:8} | [{module}] | {req_id} | {msg}"
        return colorize(line, lvl)

    def should_include(entry: dict) -> bool:
        """Check if entry matches filters"""
        if level and entry.get('level', '').upper() != level.upper():
            return False
        if request_id and request_id not in entry.get('request_id', ''):
            return False
        if search and search.lower() not in entry.get('msg', '').lower():
            return False
        return True

    if follow:
        print(f"Following {JSON_LOG_FILE} (Ctrl+C to stop)...")
        try:
            with open(JSON_LOG_FILE, 'r') as f:
                f.seek(0, 2)
                while True:
                    line = f.readline()
                    if line:
                        try:
                            entry = json.loads(line.strip())
                            if should_include(entry):
                                print(format_entry(entry))
                        except json.JSONDecodeError:
                            pass
                    else:
                        time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nStopped following.")
    else:
        with open(JSON_LOG_FILE, 'r') as f:
            all_lines = f.readlines()

        entries = []
        for line in all_lines[-lines * 2:]:  # Read extra in case of filtering
            try:
                entry = json.loads(line.strip())
                if should_include(entry):
                    entries.append(entry)
            except json.JSONDecodeError:
                continue

        for entry in entries[-lines:]:
            print(format_entry(entry))


def main():
    parser = argparse.ArgumentParser(description='View application logs')
    parser.add_argument('--lines', '-n', type=int, default=50, help='Number of lines (default: 50)')
    parser.add_argument('--level', '-l', type=str, help='Filter by level (ERROR, WARNING, INFO, DEBUG)')
    parser.add_argument('--request-id', '-r', type=str, help='Filter by request ID')
    parser.add_argument('--search', '-s', type=str, help='Search in log messages')
    parser.add_argument('--follow', '-f', action='store_true', help='Follow mode (like tail -f)')
    parser.add_argument('--json', '-j', action='store_true', help='Use JSON log file')
    args = parser.parse_args()

    # Default to JSON logs if available
    use_json = args.json or JSON_LOG_FILE.exists()

    if use_json:
        view_json_logs(args.lines, args.level, args.request_id, args.search, args.follow)
    else:
        view_text_logs(args.lines, args.level, args.request_id, args.search, args.follow)


if __name__ == '__main__':
    main()
