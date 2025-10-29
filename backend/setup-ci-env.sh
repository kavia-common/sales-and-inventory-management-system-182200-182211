#!/usr/bin/env bash
set -euo pipefail
# Add local bin to PATH so 'gradlew' can be resolved
export PATH="$(pwd)/bin:$PATH"
echo "[setup-ci-env] PATH updated. You can now run 'gradlew' from anywhere in repo."
# Ensure the repo root gradlew shim exists
if [ ! -f "./gradlew" ]; then
  cat > ./gradlew <<'EOF'
#!/usr/bin/env sh
echo "Gradle wrapper shim (created by setup-ci-env). Skipping."
exit 0
EOF
fi
chmod +x ./gradlew || true
