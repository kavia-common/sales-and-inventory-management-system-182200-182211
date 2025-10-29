Security Notes

- This backend exposes public endpoints without authentication for prototype/demo.
- For production, add authentication/authorization (e.g., API keys or OAuth2).
- Do not expose database credentials publicly; use environment variables (.env not committed).
- CORS can be restricted via CORS_ALLOW_ORIGINS in .env.
- Error handling: unhandled exceptions return JSON 500 without stack traces by default.
