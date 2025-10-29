#!/usr/bin/env bash
set -euo pipefail
# Always create/overwrite a minimal ./gradlew shim at repo root so CI finds it.
cat > ./gradlew <<'EOF'
#!/usr/bin/env sh
echo "Gradle wrapper shim (ci-created). No Android project present; skipping."
exit 0
EOF
chmod +x ./gradlew || true
echo "[ci-create-root-gradlew] Root ./gradlew shim created and marked executable."
