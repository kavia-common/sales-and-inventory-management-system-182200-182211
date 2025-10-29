#!/usr/bin/env bash
set -euo pipefail

# Always execute from repo root
cd "$(dirname "$0")"

# Determine Gradle distribution URL from Android project wrapper properties
WRAPPER_PROPS="sales-and-inventory-management-system-182200-182209/mobile_frontend/gradle/wrapper/gradle-wrapper.properties"
if [ ! -f "$WRAPPER_PROPS" ]; then
  echo "Cannot find $WRAPPER_PROPS. Aborting."
  exit 1
fi
DIST_URL=$(grep "^distributionUrl=" "$WRAPPER_PROPS" | sed 's/distributionUrl=//')
if [ -z "$DIST_URL" ]; then
  echo "distributionUrl missing in $WRAPPER_PROPS"
  exit 1
fi

# Download Gradle distribution if missing and expose a gradle binary in .gradle-dist/bin/gradle
CACHE_DIR=".gradle-dist"
mkdir -p "$CACHE_DIR"
ZIP_NAME=$(basename "$DIST_URL")
ZIP_PATH="$CACHE_DIR/$ZIP_NAME"
if [ ! -f "$ZIP_PATH" ]; then
  echo "[bootstrap] Downloading Gradle: $DIST_URL"
  curl -L --fail -o "$ZIP_PATH" "$DIST_URL"
fi

EXTRACT_DIR="$CACHE_DIR/extracted"
if [ ! -d "$EXTRACT_DIR" ]; then
  mkdir -p "$EXTRACT_DIR"
  echo "[bootstrap] Extracting Gradle to $EXTRACT_DIR"
  unzip -q "$ZIP_PATH" -d "$EXTRACT_DIR"
fi

# Find the gradle dir gradle-X.Y
GRADLE_HOME=$(find "$EXTRACT_DIR" -maxdepth 1 -type d -name "gradle-*" | head -n 1)
if [ -z "$GRADLE_HOME" ]; then
  echo "Unable to locate extracted Gradle home."
  exit 1
fi

GRADLE_BIN="$GRADLE_HOME/bin/gradle"
chmod +x "$GRADLE_BIN" || true

# Run Gradle directly without wrapper against the Android settings at repo root (mapped in settings.gradle)
echo "[bootstrap] Running Gradle tests using $GRADLE_BIN"
"$GRADLE_BIN" :mobile_frontend_app:test
