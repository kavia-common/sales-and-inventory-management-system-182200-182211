Notice for CI Maintainers

Your pipeline is invoking ./gradlew directly and failing because no Gradle Wrapper JAR is checked in.

Use one of these entry points from repository root:
- bash run_mobile_ci_bootstrap.sh           # preferred; downloads Gradle and runs tests
- bash .ci/init.sh && ./gradlew :mobile_frontend_app:test
- bash create_temp_gradle_wrapper_and_test.sh

Ensure your CI runs from repository root.
