# CI Gradle Shim Notes (Backend Workspace)

Some CI environments set the working directory to the backend workspace and invoke `../mobile_frontend/gradlew`. To prevent failures, a shim is provided at:

- `sales-and-inventory-management-system-182200-182211/mobile_frontend/gradlew*`

It forwards to the actual mobile container workspace:
- `sales-and-inventory-management-system-182200-182209/mobile_frontend/gradlew*`

For best results, run from repo root:
```
bash ./prepare-ci-shims.sh
bash ./run-mobile-ci.sh
```
