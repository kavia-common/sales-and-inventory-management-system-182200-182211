import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from dotenv import load_dotenv

load_dotenv()

# SQLAlchemy Base
Base = declarative_base()

# Build DB URL from environment; defaults designed for preview
DB_USER = os.getenv("MYSQL_USER", "root")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
DB_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
DB_PORT = os.getenv("MYSQL_PORT", "5001")  # as specified in requirements
DB_NAME = os.getenv("MYSQL_DB", "sales_inventory_db")

# Using mysql+mysqlclient driver string; ensure dependency installed
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"mysql+mysqlclient://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
)

# Create engine and session
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# PUBLIC_INTERFACE
def get_db() -> Generator[Session, None, None]:
    """Provide a SQLAlchemy session per request."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# PUBLIC_INTERFACE
def init_db():
    """Create database tables if they do not exist."""
    # Import models within function scope to register mappings without unused import at module level
    from . import models  # noqa: F401
    Base.metadata.create_all(bind=engine)
