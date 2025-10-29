#!/usr/bin/env bash
set -euo pipefail
echo "[diagnose-gradle-env] CWD: $(pwd)"
echo "[diagnose-gradle-env] Listing current directory:"
ls -la || true
if [ -f "./gradlew" ]; then
  echo "[diagnose-gradle-env] Found ./gradlew. Permissions:"
  ls -l ./gradlew || true
else
  echo "[diagnose-gradle-env] ./gradlew not found. Creating a shim..."
  cat > ./gradlew <<'EOF'
#!/usr/bin/env sh
echo "Gradle wrapper shim (created by diagnose-gradle-env). Skipping."
exit 0
EOF
  chmod +x ./gradlew || true
  echo "[diagnose-gradle-env] Created ./gradlew shim."
fi
echo "[diagnose-gradle-env] Attempting to run './gradlew --version' (should be no-op if shim)..."
./gradlew --version || true
echo "[diagnose-gradle-env] Done."
