# Gradle Wrapper

This project includes wrapper shims (`gradlew`, `gradlew.bat`) that will use the Gradle Wrapper if its JAR exists at `gradle/wrapper/gradle-wrapper.jar`. If not present, they fall back to `gradle` on PATH.

To generate the official Gradle Wrapper:
1. Ensure Gradle is installed locally (`gradle -v`).
2. From this directory, run:
   ```
   gradle wrapper --gradle-version 8.7
   ```
3. Commit the generated files, including:
   - `gradle/wrapper/gradle-wrapper.jar` (binary)
   - Updated `gradle/wrapper/gradle-wrapper.properties`
   - Updated `gradlew` and `gradlew.bat` scripts (if changed)
