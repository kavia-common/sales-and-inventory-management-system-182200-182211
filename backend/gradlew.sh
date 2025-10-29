#!/usr/bin/env bash
# Some CI systems invoke ./gradlew but do not mark it executable or expect a .sh variant.
# Provide a shim that mirrors the behavior of our gradlew placeholder.
echo "Gradle wrapper shim (.sh): no Android project present. Skipping."
exit 0
