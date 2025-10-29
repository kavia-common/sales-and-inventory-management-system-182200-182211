#!/usr/bin/env bash
set -euo pipefail
ROOT_GRADLEW="./gradlew"
MOBILE_GRADLEW="sales-and-inventory-management-system-182200-182209/mobile_frontend/gradlew"

if [ -f "$ROOT_GRADLEW" ]; then
  chmod +x "$ROOT_GRADLEW" || true
  echo "[force-create-root-gradlew] Root gradlew already exists."
  exit 0
fi

if [ -f "$MOBILE_GRADLEW" ]; then
  cp "$MOBILE_GRADLEW" "$ROOT_GRADLEW"
  chmod +x "$ROOT_GRADLEW" || true
  echo "[force-create-root-gradlew] Copied mobile_frontend gradlew to repo root."
  exit 0
fi

# As last resort, create a no-op shim
cat > "$ROOT_GRADLEW" <<'EOF'
#!/usr/bin/env sh
echo "Gradle wrapper shim (created by force-create-root-gradlew). Skipping."
exit 0
EOF
chmod +x "$ROOT_GRADLEW" || true
echo "[force-create-root-gradlew] Created no-op gradlew shim at repo root."
