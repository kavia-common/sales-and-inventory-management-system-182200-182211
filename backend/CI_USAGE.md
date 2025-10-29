CI Usage:

Use one of these from the repository root:
- bash run_all_ci.sh
- bash sales-and-inventory-management-system-182200-182209/run_mobile_no_wrapper.sh :app:test
- bash prepare_ci_and_build_mobile.sh

Avoid invoking ./gradlew directly from the repository root. If your CI requires ./gradlew,
ensure it runs in sales-and-inventory-management-system-182200-182209/mobile_frontend and use the local shim:
- chmod +x sales-and-inventory-management-system-182200-182209/mobile_frontend/gradlew
- (cd sales-and-inventory-management-system-182200-182209/mobile_frontend && ./gradlew :app:test)
