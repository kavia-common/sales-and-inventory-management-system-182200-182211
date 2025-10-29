Mobile Backend URLs

- Android emulator: http://10.0.2.2:3001/
- Real device on same network: http://<your-host-ip>:3001/
- Local dev browser/desktop: http://localhost:3001/

CORS:
- Configure allowed origins via backend env CORS_ALLOW_ORIGINS (CSV).
- Example: CORS_ALLOW_ORIGINS=http://localhost:3000,http://10.0.2.2:3001
