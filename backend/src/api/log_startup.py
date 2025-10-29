from .startup_log import get_startup_info

# PUBLIC_INTERFACE
def log_startup():
    """This is a public function."""
    info = get_startup_info()
    print(f"[backend] Starting on port {info['port']}, DB={info['database_url']}, CORS={info['cors_allow_origins']}")
