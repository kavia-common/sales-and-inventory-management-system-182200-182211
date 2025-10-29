Use the temporary wrapper script to run Android Gradle tasks without relying on ./gradlew:

From repository root:
- bash create_temp_gradle_wrapper_and_test.sh

This downloads the configured Gradle distribution and runs :mobile_frontend_app:test using the root-level settings mapping.
