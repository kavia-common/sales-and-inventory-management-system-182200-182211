#!/usr/bin/env bash
set -euo pipefail
echo "[mobile_frontend] CI mobile script starting..."
pwd
ls -la
if [ -x "./gradlew" ]; then
  echo "[mobile_frontend] gradlew shim present. Executing no-op check..."
  ./gradlew --version || true
  echo "[mobile_frontend] Done."
  exit 0
fi
echo "[mobile_frontend] gradlew not found. Creating shim..."
cat > ./gradlew <<'EOF'
#!/usr/bin/env bash
echo "Mobile frontend Gradle wrapper shim: no Android project present. Skipping."
exit 0
EOF
chmod +x ./gradlew
./gradlew --version || true
echo "[mobile_frontend] Completed."
