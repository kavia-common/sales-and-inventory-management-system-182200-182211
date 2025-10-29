Android Build Environment

- Java: 17
- Gradle: 8.7 (as per distributionUrl in gradle-wrapper.properties)
- Android Gradle Plugin: 8.4.2 (see mobile_frontend/build.gradle.kts)

If using Android emulator:
- Backend base URL is http://10.0.2.2:3001/

To run tests from repo root without relying on ./gradlew:
- bash run_mobile_ci_bootstrap.sh
