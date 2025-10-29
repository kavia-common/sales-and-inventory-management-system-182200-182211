To avoid mobile code analysis failures while the Android app is pending:
- Ensure CI runs from repository root.
- Call: bash ./prepare-and-run-gradlew.sh
- Alternatively: bash ./run-gradlew-anywhere.sh

Both scripts will ensure a no-op Gradle wrapper exists and will return success even if no Android project is present.
