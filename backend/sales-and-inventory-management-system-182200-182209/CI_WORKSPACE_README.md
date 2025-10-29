# Mobile Container Workspace CI

If CI sets working dir to:
```
sales-and-inventory-management-system-182200-182209/
```

You can invoke:
```
./gradlew   # (provided via shim in this workspace or in mobile_frontend)
./gradlew.sh
mobile_frontend/gradlew
```

Before running, ensure execute permissions (CI step):
```
bash ../../prepare-ci-shims.sh || true
chmod +x ./gradlew.sh || true
chmod +x mobile_frontend/gradlew || true
```

These are placeholders; replace with a full Android project and standard Gradle wrapper in future.
