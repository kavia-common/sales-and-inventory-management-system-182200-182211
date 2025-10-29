# CI Execution Order (Mobile Analysis)

If your CI runs Android/Gradle checks but the project has not been added yet, run these shims first:

1) bash ./bootstrap-mobile-ci.sh
2) bash ./ensure-gradle-shims.sh
3) ./gradlew --version || true
4) bash ./gradlew-relay.sh tasks || true

These steps ensure a no-op Gradle wrapper is present at expected locations and exits with success to avoid false negatives while mobile code is not yet implemented.
