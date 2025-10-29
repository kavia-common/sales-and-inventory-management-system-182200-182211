#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Read distributionUrl from wrapper properties
DIST_URL=$(grep "^distributionUrl=" gradle/wrapper/gradle-wrapper.properties | sed 's/distributionUrl=//')
if [ -z "$DIST_URL" ]; then
  echo "distributionUrl not found in gradle/wrapper/gradle-wrapper.properties"
  exit 1
fi

GRADLE_ZIP_NAME=$(basename "$DIST_URL")
GRADLE_DIR="${GRADLE_ZIP_NAME%.zip}"
CACHE_DIR="${HOME}/.gradle-dists"
INSTALL_DIR="${CACHE_DIR}/${GRADLE_DIR}"

mkdir -p "$CACHE_DIR"

# Download Gradle distribution if needed
if [ ! -d "$INSTALL_DIR" ]; then
  echo "Downloading Gradle from $DIST_URL ..."
  TMP_ZIP="${CACHE_DIR}/${GRADLE_ZIP_NAME}"
  curl -L --fail -o "$TMP_ZIP" "$DIST_URL"
  echo "Extracting to $INSTALL_DIR ..."
  mkdir -p "$INSTALL_DIR"
  unzip -q "$TMP_ZIP" -d "$CACHE_DIR"
  # Move extracted folder to INSTALL_DIR if unzip created a new folder
  if [ -d "${CACHE_DIR}/${GRADLE_DIR}" ]; then
    :
  else
    # find the extracted directory starting with gradle-
    EXTRACTED=$(find "$CACHE_DIR" -maxdepth 1 -type d -name "gradle-*" | head -n 1)
    mv "$EXTRACTED" "$INSTALL_DIR"
  fi
fi

# Run Gradle using the downloaded distribution
GRADLE_BIN="${INSTALL_DIR}/bin/gradle"
chmod +x "$GRADLE_BIN" || true

# Pass through all arguments (e.g., assembleDebug, test)
exec "$GRADLE_BIN" "$@"
