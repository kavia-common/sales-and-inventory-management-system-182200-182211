# Mobile Frontend Placeholder

The Android project is not yet implemented. CI environments may still invoke `./gradlew` inside this directory.

Included shims:
- `./gradlew`: Bash shim that exits 0
- `./gradlew.bat`: Windows shim that exits 0
- `./ci-mobile.sh`: Entry script to run gradle shim and print environment info

Once the Android project is added, replace these with the real Gradle wrapper and project files.
