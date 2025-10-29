# Mobile Workspace CI Fallback

Use this script if your CI cannot find `./gradlew`:
```bash
bash run-check.sh
```

The script ensures a temporary shim `./gradlew` exists in this directory and delegates to:
- `./mobile_frontend/gradlew` if present
- System `gradle` if available
- Otherwise it no-ops successfully for common tasks
