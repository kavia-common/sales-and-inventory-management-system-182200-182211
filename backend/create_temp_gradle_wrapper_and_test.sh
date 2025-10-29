#!/usr/bin/env bash
set -euo pipefail

# Use Gradle version from mobile_frontend wrapper config
WRAPPER_PROPS="sales-and-inventory-management-system-182200-182209/mobile_frontend/gradle/wrapper/gradle-wrapper.properties"
if [ ! -f "$WRAPPER_PROPS" ]; then
  echo "Wrapper properties not found at $WRAPPER_PROPS"
  exit 1
fi
DIST_URL=$(grep "^distributionUrl=" "$WRAPPER_PROPS" | sed 's/distributionUrl=//')
if [ -z "$DIST_URL" ]; then
  echo "distributionUrl missing in wrapper properties"
  exit 1
fi

# Prepare temp wrapper dir
TMP_DIR=".temp-gradle-wrapper"
mkdir -p "$TMP_DIR"
ZIP_NAME=$(basename "$DIST_URL")
ZIP_PATH="$TMP_DIR/$ZIP_NAME"

# Download Gradle distribution
if [ ! -f "$ZIP_PATH" ]; then
  echo "[temp-wrapper] Downloading Gradle: $DIST_URL"
  curl -L --fail -o "$ZIP_PATH" "$DIST_URL"
fi

# Extract
EXTRACT_DIR="$TMP_DIR/extracted"
mkdir -p "$EXTRACT_DIR"
if [ -z "$(ls -A "$EXTRACT_DIR")" ]; then
  echo "[temp-wrapper] Extracting Gradle to $EXTRACT_DIR"
  unzip -q "$ZIP_PATH" -d "$EXTRACT_DIR"
fi

# Locate gradle bin
GRADLE_HOME=$(find "$EXTRACT_DIR" -maxdepth 1 -type d -name "gradle-*" | head -n 1)
if [ -z "$GRADLE_HOME" ]; then
  echo "Unable to locate extracted Gradle home."
  exit 1
fi
GRADLE_BIN="$GRADLE_HOME/bin/gradle"
chmod +x "$GRADLE_BIN" || true

# Run tests pointing to the root-level settings which maps to the app module
echo "[temp-wrapper] Running Gradle tests..."
"$GRADLE_BIN" :mobile_frontend_app:test
