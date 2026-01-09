#!/usr/bin/env python3
"""
Execute SQL queries against Beslist.nl Redshift database.

Usage:
    python scripts/run_query.py "SELECT * FROM table LIMIT 10"
    python scripts/run_query.py --file query.sql
    python scripts/run_query.py --file query.sql --output results.csv
"""

import os
import sys
import argparse
from pathlib import Path

# Load .env from skill directory
skill_dir = Path(__file__).parent.parent
env_file = skill_dir / '.env'

def load_env():
    """Load environment variables from .env file."""
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    # Remove quotes from value
                    value = value.strip().strip("'").strip('"')
                    os.environ[key] = value

load_env()

def get_connection():
    """Create Redshift connection using credentials from .env."""
    try:
        import psycopg2
    except ImportError:
        print("ERROR: psycopg2 not installed. Install with: pip install psycopg2-binary", file=sys.stderr)
        sys.exit(1)

    host = os.environ.get('REDSHIFT_HOST')
    port = os.environ.get('REDSHIFT_PORT', '5439')
    database = os.environ.get('REDSHIFT_DATABASE')
    user = os.environ.get('REDSHIFT_USER')
    password = os.environ.get('REDSHIFT_PASSWORD')

    if not host:
        print("ERROR: REDSHIFT_HOST not set. Uncomment it in .env file.", file=sys.stderr)
        sys.exit(1)

    if not all([database, user, password]):
        print("ERROR: Missing Redshift credentials in .env file.", file=sys.stderr)
        sys.exit(1)

    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        return conn
    except Exception as e:
        print(f"ERROR: Could not connect to Redshift: {e}", file=sys.stderr)
        sys.exit(1)

def run_query(query: str, output_file: str = None):
    """Execute query and return results."""
    import pandas as pd

    conn = get_connection()

    try:
        df = pd.read_sql_query(query, conn)

        if output_file:
            if output_file.endswith('.csv'):
                df.to_csv(output_file, index=False)
            elif output_file.endswith('.json'):
                df.to_json(output_file, orient='records', indent=2)
            else:
                df.to_csv(output_file, index=False)
            print(f"Results saved to {output_file}")

        return df
    finally:
        conn.close()

def main():
    parser = argparse.ArgumentParser(description='Execute Redshift queries')
    parser.add_argument('query', nargs='?', help='SQL query to execute')
    parser.add_argument('--file', '-f', help='Read query from file')
    parser.add_argument('--output', '-o', help='Save results to file (csv/json)')
    parser.add_argument('--limit', '-l', type=int, help='Limit results (adds LIMIT clause)')

    args = parser.parse_args()

    if args.file:
        with open(args.file) as f:
            query = f.read()
    elif args.query:
        query = args.query
    else:
        print("ERROR: Provide a query or use --file", file=sys.stderr)
        sys.exit(1)

    if args.limit and 'LIMIT' not in query.upper():
        query = query.rstrip(';') + f' LIMIT {args.limit}'

    df = run_query(query, args.output)

    # Print results summary
    print(f"\n=== Query Results ===")
    print(f"Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print(f"\n{df.to_string()}")

    return df

if __name__ == '__main__':
    main()
