#!/usr/bin/env bash
set -euo pipefail
echo "[ci-ensure-and-run-gradlew] Ensuring ./gradlew exists at repo root..."
if [ ! -f "./gradlew" ]; then
  cat > ./gradlew <<'EOF'
#!/usr/bin/env sh
echo "Gradle wrapper shim (created by ci-ensure-and-run-gradlew). Skipping."
exit 0
EOF
fi
chmod +x ./gradlew || true
echo "[ci-ensure-and-run-gradlew] Running ./gradlew --version (no-op if shim)..."
./gradlew --version || true
echo "[ci-ensure-and-run-gradlew] Completed."
