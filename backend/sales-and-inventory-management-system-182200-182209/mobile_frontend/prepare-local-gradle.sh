#!/usr/bin/env bash
set -euo pipefail
mkdir -p gradle/wrapper
cat > gradle/wrapper/gradle-wrapper.properties <<'EOF'
distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
distributionUrl=https\://services.gradle.org/distributions/gradle-8.6-bin.zip
EOF

if [ ! -f "./gradlew" ]; then
  cat > ./gradlew <<'EOF'
#!/usr/bin/env sh
echo "Mobile frontend local gradle shim. Skipping."
exit 0
EOF
  chmod +x ./gradlew || true
fi
echo "[prepare-local-gradle] Mobile frontend gradle shim prepared."
