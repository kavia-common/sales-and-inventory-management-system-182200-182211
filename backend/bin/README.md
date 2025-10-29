Use ./bin/gradlew as the Gradle entry in CI if the runner cannot execute ./gradlew directly.
It ensures the root ./gradlew shim is executable and delegates to it.
Example:
- bash ./bin/gradlew :mobile_frontend_app:test
