Mobile CI Guide

If your CI fails with: "./gradlew: No such file or directory", use one of these from the repository root:

Preferred (no wrapper needed):
- bash run_mobile_ci_bootstrap.sh
- bash create_temp_gradle_wrapper_and_test.sh

Alternative using Gradle shim (ensure exec perms first):
- bash .ci/init.sh && ./gradlew :mobile_frontend_app:test

Other aliases:
- bash CI_ENTRYPOINT.sh
- bash test.sh
- bash gradlew-run.sh
- bash build_android.sh

Notes:
- Ensure working directory is repository root.
- Java 17 required (AGP 8.4.2, Gradle 8.7).
- Android SDK is not required for unit tests; for full builds, accept licenses and install build-tools.
