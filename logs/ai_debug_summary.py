#!/usr/bin/env python3
"""
AI Debug Summary - Quick diagnostic entry point for Claude

Run this to get a structured overview of recent logs and issues.
Claude can parse this output to quickly understand system state.

Usage:
    python logs/ai_debug_summary.py
    python logs/ai_debug_summary.py --hours 1
    python logs/ai_debug_summary.py --errors-only
    python logs/ai_debug_summary.py --json
"""

import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from typing import List, Dict, Any

# Find project root and log directory
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
LOG_DIR = PROJECT_ROOT / "logs"
JSON_LOG_FILE = LOG_DIR / "application.jsonl"


def parse_logs(hours: int = 24, errors_only: bool = False) -> List[Dict[str, Any]]:
    """Parse JSON logs from the last N hours"""
    if not JSON_LOG_FILE.exists():
        return []

    cutoff = datetime.utcnow() - timedelta(hours=hours)
    cutoff_str = cutoff.isoformat() + "Z"

    logs = []
    with open(JSON_LOG_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                if entry.get('ts', '') >= cutoff_str:
                    if errors_only and entry.get('level') != 'ERROR':
                        continue
                    logs.append(entry)
            except json.JSONDecodeError:
                continue

    return logs


def analyze_errors(logs: List[Dict]) -> Dict[str, Any]:
    """Analyze error patterns"""
    errors = [log for log in logs if log.get('level') == 'ERROR']

    # Group by exception type
    by_exception = defaultdict(list)
    for error in errors:
        exc_type = error.get('exception', {}).get('type') or 'Unknown'
        by_exception[exc_type].append(error)

    # Group by module
    by_module = defaultdict(int)
    for error in errors:
        by_module[error.get('module', 'Unknown')] += 1

    return {
        "total_errors": len(errors),
        "by_exception_type": {k: len(v) for k, v in by_exception.items()},
        "by_module": dict(by_module),
        "recent_errors": [
            {
                "ts": e.get('ts'),
                "module": e.get('module'),
                "msg": e.get('msg', '')[:150],
                "exception": e.get('exception', {}).get('type'),
                "request_id": e.get('request_id')
            }
            for e in errors[-10:]  # Last 10 errors
        ]
    }


def analyze_performance(logs: List[Dict]) -> Dict[str, Any]:
    """Analyze performance from span logs"""
    spans = [log for log in logs if log.get('span_op') and log.get('duration_ms')]

    if not spans:
        return {"message": "No span data found"}

    # Group by operation
    by_operation = defaultdict(list)
    for span in spans:
        by_operation[span['span_op']].append(span['duration_ms'])

    # Calculate stats per operation
    stats = {}
    for op, durations in by_operation.items():
        stats[op] = {
            "count": len(durations),
            "avg_ms": round(sum(durations) / len(durations), 2),
            "max_ms": round(max(durations), 2),
            "min_ms": round(min(durations), 2)
        }

    # Find slow operations (> 2 seconds)
    slow = [
        {"operation": s['span_op'], "duration_ms": s['duration_ms'], "request_id": s.get('request_id')}
        for s in spans if s['duration_ms'] > 2000
    ]

    return {
        "total_spans": len(spans),
        "operations": stats,
        "slow_operations": sorted(slow, key=lambda x: x['duration_ms'], reverse=True)[:10]
    }


def suggest_investigations(error_analysis: Dict) -> List[str]:
    """Generate investigation suggestions based on errors"""
    suggestions = []

    if error_analysis['total_errors'] == 0:
        return ["No errors found - system appears healthy"]

    # High error count
    if error_analysis['total_errors'] > 10:
        suggestions.append(f"HIGH: {error_analysis['total_errors']} errors detected - investigate immediately")

    # Specific exception patterns
    exc_types = error_analysis.get('by_exception_type', {})

    if 'ConnectionError' in exc_types or 'TimeoutError' in exc_types:
        suggestions.append("Network/connection issues detected - check external service availability")

    if 'DatabaseError' in exc_types or 'OperationalError' in exc_types:
        suggestions.append("Database errors detected - check connection pool and query performance")

    if 'ValidationError' in exc_types or 'ValueError' in exc_types:
        suggestions.append("Validation errors detected - check input data format and constraints")

    if 'KeyError' in exc_types or 'AttributeError' in exc_types:
        suggestions.append("Data structure errors detected - check for None values or missing fields")

    if 'HTTPException' in exc_types:
        suggestions.append("HTTP errors detected - check API endpoints and request handling")

    # Module-specific suggestions
    modules = error_analysis.get('by_module', {})
    if 'FRONTEND' in modules and modules['FRONTEND'] > 3:
        suggestions.append(f"Frontend has {modules['FRONTEND']} errors - check browser console for details")

    if 'DATABASE' in modules and modules['DATABASE'] > 0:
        suggestions.append("Database module errors - check connection and query syntax")

    return suggestions if suggestions else ["Review recent errors for patterns"]


def generate_summary(hours: int = 24) -> Dict[str, Any]:
    """Generate complete debug summary"""
    logs = parse_logs(hours=hours)

    if not logs:
        return {
            "status": "NO_LOGS",
            "message": f"No logs found in the last {hours} hours",
            "log_file": str(JSON_LOG_FILE),
            "log_file_exists": JSON_LOG_FILE.exists()
        }

    # Basic stats
    level_counts = defaultdict(int)
    module_counts = defaultdict(int)
    request_ids = set()

    for log in logs:
        level_counts[log.get('level', 'UNKNOWN')] += 1
        module_counts[log.get('module', 'UNKNOWN')] += 1
        if log.get('request_id') and log['request_id'] != '----':
            request_ids.add(log['request_id'])

    error_analysis = analyze_errors(logs)
    performance = analyze_performance(logs)
    suggestions = suggest_investigations(error_analysis)

    # Determine health status
    error_rate = error_analysis['total_errors'] / len(logs) if logs else 0
    if error_rate > 0.1:
        health = "CRITICAL"
    elif error_rate > 0.05:
        health = "WARNING"
    elif error_analysis['total_errors'] > 0:
        health = "DEGRADED"
    else:
        health = "HEALTHY"

    return {
        "status": health,
        "time_range": {
            "hours_analyzed": hours,
            "oldest_log": logs[0].get('ts') if logs else None,
            "newest_log": logs[-1].get('ts') if logs else None
        },
        "overview": {
            "total_logs": len(logs),
            "unique_requests": len(request_ids),
            "error_rate": f"{error_rate:.1%}"
        },
        "level_distribution": dict(level_counts),
        "module_distribution": dict(module_counts),
        "errors": error_analysis,
        "performance": performance,
        "suggestions": suggestions,
        "quick_commands": {
            "view_errors": "python logs/view_logs.py --level ERROR",
            "view_request": "python logs/view_logs.py --request-id <ID>",
            "api_errors": "curl 'localhost:8001/api/debug/logs?level=ERROR&last=20'",
            "api_summary": "curl 'localhost:8001/api/debug/logs?since_minutes=60&include_summary=true'",
            "follow_logs": "python logs/view_logs.py --follow"
        }
    }


def main():
    parser = argparse.ArgumentParser(description='AI Debug Summary - Quick diagnostic for Claude')
    parser.add_argument('--hours', type=int, default=24, help='Hours to analyze (default: 24)')
    parser.add_argument('--errors-only', action='store_true', help='Only show error analysis')
    parser.add_argument('--json', action='store_true', help='Output raw JSON (for AI parsing)')
    args = parser.parse_args()

    summary = generate_summary(hours=args.hours)

    if args.json:
        print(json.dumps(summary, indent=2, default=str))
        return

    # Human-readable output
    print("=" * 70)
    print(f"AI DEBUG SUMMARY - Last {args.hours} hours")
    print("=" * 70)
    print()

    # Health status with color
    status = summary.get('status', 'UNKNOWN')
    status_colors = {
        'HEALTHY': '\033[92m',  # Green
        'DEGRADED': '\033[93m',  # Yellow
        'WARNING': '\033[93m',  # Yellow
        'CRITICAL': '\033[91m',  # Red
        'NO_LOGS': '\033[90m',  # Gray
    }
    reset = '\033[0m'
    print(f"Status: {status_colors.get(status, '')}{status}{reset}")
    print()

    if status == 'NO_LOGS':
        print(summary.get('message', 'No logs found'))
        print(f"Log file: {summary.get('log_file')}")
        print(f"Exists: {summary.get('log_file_exists')}")
        return

    # Overview
    overview = summary.get('overview', {})
    print(f"Total Logs: {overview.get('total_logs', 0)}")
    print(f"Unique Requests: {overview.get('unique_requests', 0)}")
    print(f"Error Rate: {overview.get('error_rate', '0%')}")
    print()

    # Time range
    time_range = summary.get('time_range', {})
    if time_range.get('oldest_log'):
        print(f"Time Range: {time_range.get('oldest_log')} to {time_range.get('newest_log')}")
        print()

    # Level distribution
    print("Log Levels:")
    for level, count in summary.get('level_distribution', {}).items():
        color = {'ERROR': '\033[91m', 'WARNING': '\033[93m', 'INFO': '\033[92m'}.get(level, '')
        print(f"  {color}{level}{reset}: {count}")
    print()

    # Module distribution
    print("Modules:")
    for module, count in summary.get('module_distribution', {}).items():
        print(f"  {module}: {count}")
    print()

    # Errors
    errors = summary.get('errors', {})
    if errors.get('total_errors', 0) > 0:
        print(f"\033[91mERRORS ({errors['total_errors']} total):\033[0m")
        for exc_type, count in errors.get('by_exception_type', {}).items():
            print(f"  {exc_type}: {count}")
        print()
        print("Recent Errors:")
        for err in errors.get('recent_errors', [])[-5:]:
            print(f"  [{err.get('ts', '')[:19]}] {err.get('module', '')}: {err.get('msg', '')[:60]}...")
        print()

    # Performance
    performance = summary.get('performance', {})
    if performance.get('total_spans'):
        print(f"Performance ({performance['total_spans']} spans):")
        for op, stats in performance.get('operations', {}).items():
            print(f"  {op}: avg={stats['avg_ms']}ms, max={stats['max_ms']}ms ({stats['count']} calls)")
        slow = performance.get('slow_operations', [])
        if slow:
            print(f"\n  Slow operations (>2s): {len(slow)}")
            for s in slow[:3]:
                print(f"    - {s['operation']}: {s['duration_ms']:.0f}ms")
        print()

    # Suggestions
    suggestions = summary.get('suggestions', [])
    if suggestions:
        print("\033[93mSUGGESTED INVESTIGATIONS:\033[0m")
        for s in suggestions:
            print(f"  - {s}")
        print()

    # Quick commands
    print("Quick Commands:")
    for name, cmd in summary.get('quick_commands', {}).items():
        print(f"  {name}: {cmd}")


if __name__ == '__main__':
    main()
