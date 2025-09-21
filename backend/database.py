import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    """Simple database connection for small apps"""
    return psycopg2.connect(
        os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/myapp"),
        cursor_factory=RealDictCursor
    )

def init_db():
    """Initialize database tables"""
    conn = get_db_connection()
    cur = conn.cursor()

    # Create your tables here
    cur.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Database initialized")

if __name__ == "__main__":
    init_db()
