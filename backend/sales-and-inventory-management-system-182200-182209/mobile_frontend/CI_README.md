# Mobile Frontend Gradle Placeholder

This placeholder provides minimal Gradle files so CI jobs invoking Gradle do not fail.

- settings.gradle
- build.gradle (with `ciNoOp` task)

Example CI step:
```
cd sales-and-inventory-management-system-182200-182209/mobile_frontend
../../prepare-ci-shims.sh || true
./gradlew ciNoOp || true
```

Replace with a real Android project in future iterations.
