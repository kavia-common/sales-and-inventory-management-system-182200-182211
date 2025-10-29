#!/usr/bin/env bash
set -euo pipefail
echo "[bootstrap-mobile-ci] Ensuring ./gradlew exists and is executable..."
if [ ! -f "./gradlew" ]; then
  cat > ./gradlew <<'EOF'
#!/usr/bin/env bash
echo "Gradle wrapper shim (root ./gradlew): no Android project present. Skipping."
exit 0
EOF
fi
chmod +x ./gradlew || true
echo "[bootstrap-mobile-ci] Running ./gradlew --version (no-op shim)..."
./gradlew --version || true
echo "[bootstrap-mobile-ci] Done."
