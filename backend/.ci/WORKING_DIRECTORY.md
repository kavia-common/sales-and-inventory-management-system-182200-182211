Run all CI steps from the repository root.

If your CI pipeline uses a working-directory setting, set it to:
.

This is required because this repository provides Gradle shims at the repository root (./gradlew) that delegate to the Android mobile module.
