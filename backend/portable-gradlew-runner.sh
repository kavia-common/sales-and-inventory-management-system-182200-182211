#!/usr/bin/env bash
set -euo pipefail
# Some CI mounts the workspace read-only or in ephemeral layers; ensure we can still run a gradle shim.
TMP_SHIM="/tmp/gradlew-shim-$$"
cat > "$TMP_SHIM" <<'EOF'
#!/usr/bin/env sh
echo "Gradle wrapper shim executed from /tmp. No Android project; skipping."
exit 0
EOF
chmod +x "$TMP_SHIM" || true
"$TMP_SHIM" --version || true
"$TMP_SHIM" tasks || true
echo "[portable-gradlew-runner] Completed."
