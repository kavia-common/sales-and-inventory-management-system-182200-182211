import os
from typing import Dict

# PUBLIC_INTERFACE
def get_startup_info() -> Dict[str, str]:
    """This is a public function."""
    db_url = os.getenv("DATABASE_URL", "")
    if not db_url:
        db_url = f"mysql+mysqlclient://{os.getenv('MYSQL_USER','root')}:***@{os.getenv('MYSQL_HOST','127.0.0.1')}:{os.getenv('MYSQL_PORT','5001')}/{os.getenv('MYSQL_DB','sales_inventory_db')}"
    return {
        "port": "3001",
        "database_url": db_url,
        "cors_allow_origins": os.getenv("CORS_ALLOW_ORIGINS", "*"),
    }
