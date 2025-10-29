# CI Notes

Some CI jobs invoke `./gradlew` for mobile analysis even when the Android project is not yet present.

Use these steps:
1. bash ./prepare-ci-shims.sh
2. bash ./ci-run-mobile.sh

Both scripts are idempotent and ensure a root `./gradlew` shim exists and is executable. They also handle the mobile_frontend shim.
