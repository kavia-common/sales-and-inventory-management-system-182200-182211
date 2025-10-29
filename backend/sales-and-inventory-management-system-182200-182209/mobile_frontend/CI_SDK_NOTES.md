If your CI installs the Android SDK, ensure licenses are accepted before running Gradle:
- yes | sdkmanager --licenses

This project does not require an emulator for unit tests, but the SDK and build-tools must be available if you run full builds.
