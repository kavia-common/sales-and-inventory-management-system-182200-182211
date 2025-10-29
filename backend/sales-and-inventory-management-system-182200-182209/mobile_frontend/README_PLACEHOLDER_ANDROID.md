This is a minimal placeholder Android Gradle project to satisfy CI analyzers.
It includes:
- settings.gradle with :app module
- build.gradle with no-op default task
- gradle wrapper properties and wrapper scripts
- app/build.gradle and a minimal AndroidManifest

The project is not intended to build an APK in CI yet and avoids heavy downloads by skipping tasks when gradle is not installed.
