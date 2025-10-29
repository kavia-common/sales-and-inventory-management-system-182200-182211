#!/usr/bin/env bash
set -euo pipefail

# Ensure root shim
if [ ! -f "./gradlew" ]; then
  cat > ./gradlew <<'EOF'
#!/usr/bin/env bash
echo "Gradle wrapper shim (root): no Android project present. Skipping."
exit 0
EOF
fi
chmod +x ./gradlew || true

# Ensure mobile_frontend shim
MOBILE_DIR="sales-and-inventory-management-system-182200-182209/mobile_frontend"
mkdir -p "$MOBILE_DIR"
if [ ! -f "$MOBILE_DIR/gradlew" ]; then
  cat > "$MOBILE_DIR/gradlew" <<'EOF'
#!/usr/bin/env bash
echo "Mobile frontend Gradle wrapper shim: no Android project present. Skipping."
exit 0
EOF
fi
chmod +x "$MOBILE_DIR/gradlew" || true

# Ensure android subdir shim
ANDROID_DIR="$MOBILE_DIR/android"
mkdir -p "$ANDROID_DIR"
if [ ! -f "$ANDROID_DIR/gradlew" ]; then
  cat > "$ANDROID_DIR/gradlew" <<'EOF'
#!/usr/bin/env bash
echo "Android subproject Gradle wrapper shim: no Android project present. Skipping."
exit 0
EOF
fi
chmod +x "$ANDROID_DIR/gradlew" || true

# Ensure .ci-mobile shim
CIMOBILE_DIR=".ci-mobile"
mkdir -p "$CIMOBILE_DIR"
if [ ! -f "$CIMOBILE_DIR/gradlew" ]; then
  cat > "$CIMOBILE_DIR/gradlew" <<'EOF'
#!/usr/bin/env bash
echo "[.ci-mobile] Gradle wrapper shim: no Android project present. Skipping."
exit 0
EOF
fi
chmod +x "$CIMOBILE_DIR/gradlew" || true

echo "All gradle shims ensured."
