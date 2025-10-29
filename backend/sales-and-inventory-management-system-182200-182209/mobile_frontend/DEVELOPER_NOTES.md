Developer Notes (Android Mobile Frontend)

- Base URL (emulator): http://10.0.2.2:3001/
- Build tools: Kotlin 1.9.22, AGP 8.4.2, Gradle 8.7
- Wrapper-less Gradle usage:
  - From repo root: bash run_mobile_ci_bootstrap.sh
  - From mobile_frontend/: bash run_without_wrapper.sh :app:test
- If you must use ./gradlew:
  - Ensure you are in the repository root or mobile_frontend directory
  - chmod +x ./gradlew
  - Run your task: ./gradlew :mobile_frontend_app:test or ./gradlew :app:test (from module)
