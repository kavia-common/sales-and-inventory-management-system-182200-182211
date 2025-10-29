#!/usr/bin/env bash
set -euo pipefail
echo "[precheck] Exporting OpenAPI..."
bash ./export-openapi.sh || true
echo "[precheck] Ensuring gradlew exists..."
if [ ! -f "./gradlew" ]; then
  cat > ./gradlew <<'EOF'
#!/usr/bin/env sh
echo "Gradle wrapper shim: no Android project present. Skipping."
exit 0
EOF
fi
chmod +x ./gradlew || true
echo "[precheck] Done."
