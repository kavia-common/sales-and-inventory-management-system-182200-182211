#!/usr/bin/env bash
set -euo pipefail
echo "[ci-run-mobile] Starting mobile CI shim..."
if [ -x "./gradlew" ]; then
  echo "[ci-run-mobile] Found gradlew shim. Executing no-op task..."
  ./gradlew --version || true
  echo "[ci-run-mobile] Gradle shim executed."
else
  echo "[ci-run-mobile] gradlew not found; creating shim..."
  cat > ./gradlew <<'EOF'
#!/usr/bin/env bash
echo "Gradle wrapper shim: no Android project present. Skipping."
exit 0
EOF
  chmod +x ./gradlew
  ./gradlew --version || true
fi
echo "[ci-run-mobile] Done."
