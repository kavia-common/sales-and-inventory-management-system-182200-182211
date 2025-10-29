Your CI is attempting to run ./gradlew, but this repository intentionally avoids checking in a full Gradle Wrapper jar.

Use one of the supported entrypoints from the repository root:
- bash run_mobile_ci_bootstrap.sh
- bash .ci/init.sh && ./gradlew :mobile_frontend_app:test
- bash create_temp_gradle_wrapper_and_test.sh

Ensure the working directory is the repository root.
