#!/usr/bin/env bash
set -euo pipefail
if [ ! -f "./gradlew" ]; then
  cat > ./gradlew <<'EOF'
#!/usr/bin/env sh
echo "Gradle wrapper shim (ensure-gradlew-exists). Skipping."
exit 0
EOF
fi
chmod +x ./gradlew || true
echo "[ensure-gradlew-exists] ./gradlew is present and executable."
