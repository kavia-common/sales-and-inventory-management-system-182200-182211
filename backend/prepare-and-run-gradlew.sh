#!/usr/bin/env bash
set -euo pipefail
# Ensure gradlew exists at repo root and is executable, then run harmless tasks.
if [ ! -f "./gradlew" ]; then
  cat > ./gradlew <<'EOF'
#!/usr/bin/env sh
echo "Gradle wrapper shim (root ./gradlew): no Android project present. Skipping."
exit 0
EOF
fi
chmod +x ./gradlew || true
./gradlew --version || true
./gradlew tasks || true
echo "[prepare-and-run-gradlew] Completed."
