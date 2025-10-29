To run Gradle tasks in CI from repository root:

1) Ensure the gradle shim is executable:
   chmod +x ./gradlew

2) Run tasks (root maps to the mobile app module using settings.gradle / settings.gradle.kts):
   ./gradlew :mobile_frontend_app:test

Alternatively, bypass the wrapper entirely:
   bash run_mobile_ci_bootstrap.sh
