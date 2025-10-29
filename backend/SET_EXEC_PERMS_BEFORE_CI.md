Before running Gradle in CI, ensure the shim scripts are executable:
- chmod +x ./gradlew
- chmod +x ./gradlew.sh
- chmod +x ./gradlew.shim
- chmod +x sales-and-inventory-management-system-182200-182209/run_mobile_no_wrapper.sh
- chmod +x sales-and-inventory-management-system-182200-182209/mobile_frontend/run_without_wrapper.sh

Then run:
- ./gradlew :app:test
or
- bash sales-and-inventory-management-system-182200-182209/run_mobile_no_wrapper.sh :app:test
