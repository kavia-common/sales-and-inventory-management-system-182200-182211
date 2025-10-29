If your CI is failing with "./gradlew: No such file or directory", use one of the provided entrypoints from repo root:
- bash .ci/init.sh && ./gradlew :mobile_frontend_app:test
- bash run_mobile_ci_bootstrap.sh
- bash create_temp_gradle_wrapper_and_test.sh
- bash CI_ENTRYPOINT.sh
- bash test.sh
Or configure CI to call:
- bash gradlew-init.sh
These avoid reliance on a pre-generated Gradle wrapper while honoring the configured Gradle version in mobile_frontend.
