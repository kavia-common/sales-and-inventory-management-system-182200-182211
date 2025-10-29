import sys
from sqlalchemy import text
from src.app.db import engine

def main():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("DB_OK")
        sys.exit(0)
    except Exception as e:
        print(f"DB_ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
