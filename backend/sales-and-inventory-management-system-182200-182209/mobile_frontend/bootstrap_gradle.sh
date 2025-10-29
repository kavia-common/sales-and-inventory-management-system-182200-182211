#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

WRAPPER_JAR="gradle/wrapper/gradle-wrapper.jar"
WRAPPER_DIR="$(dirname "$WRAPPER_JAR")"
WRAPPER_PROPS="gradle/wrapper/gradle-wrapper.properties"

# Ensure wrapper jar exists; download if missing using distribution URL jar path pattern
if [ ! -f "$WRAPPER_JAR" ]; then
  mkdir -p "$WRAPPER_DIR"
  # Extract gradle version from properties
  DIST_URL=$(grep "^distributionUrl=" "$WRAPPER_PROPS" | sed 's/distributionUrl=//')
  # Expected URL example: https://services.gradle.org/distributions/gradle-8.7-bin.zip
  # Wrapper JAR download URL pattern:
  # https://services.gradle.org/distributions/gradle-<version>-bin.zip
  # The gradle wrapper jar is part of the wrapper JAR artifact; use the official repo jar URL
  # Fallback: fetch from known wrapper JAR location for the version (8.7)
  echo "Gradle distribution: $DIST_URL"
  # Download wrapper jar from Gradle GitHub release matching major version (best effort)
  # Known stable wrapper jar source (version-agnostic small jar ~60KB)
  JAR_URL="https://repo.gradle.org/gradle/libs-releases-local/org/gradle/gradle-wrapper/8.7/gradle-wrapper-8.7.jar"
  echo "Downloading Gradle wrapper jar from $JAR_URL ..."
  curl -L --fail -o "$WRAPPER_JAR" "$JAR_URL"
fi

chmod +x ./gradlew || true
exec ./gradlew "$@"
