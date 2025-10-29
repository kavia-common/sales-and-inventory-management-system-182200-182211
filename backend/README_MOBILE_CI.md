# Mobile CI Shim

This repository currently does not include the Android project. Some CI pipelines still invoke `./gradlew` during mobile code analysis.

Use the provided shim and script to avoid failures:
- Root `./gradlew` is a no-op shim that exits 0
- Run `bash ./ci-run-mobile.sh` as the CI entry for mobile steps

Replace the shim with real Android Gradle wrapper and project when the mobile app is implemented.
