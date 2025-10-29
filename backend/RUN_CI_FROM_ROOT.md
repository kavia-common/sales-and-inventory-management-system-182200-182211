Run CI from repository root.

Do NOT cd into subfolders before invoking Gradle. The repository root provides a ./gradlew shim that delegates to the Android project using a wrapper-less Gradle runner.

Examples:
- ./gradlew :app:test
- bash ensure_gradlew_and_run.sh
- bash sales-and-inventory-management-system-182200-182209/run_mobile_no_wrapper.sh :app:test
