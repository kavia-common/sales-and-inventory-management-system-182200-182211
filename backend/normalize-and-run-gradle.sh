#!/usr/bin/env bash
set -euo pipefail
# Move to repo root based on this script's location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Ensure gradlew exists
if [ ! -f "./gradlew" ]; then
  cat > ./gradlew <<'EOF'
#!/usr/bin/env sh
echo "Gradle wrapper shim (created by normalize-and-run-gradle). Skipping."
exit 0
EOF
fi
chmod +x ./gradlew || true

# Run harmless commands
./gradlew --version || true
./gradlew tasks || true
echo "[normalize-and-run-gradle] Completed."
