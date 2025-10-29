# Mobile workspace CI shims

If your CI executes `./gradlew` within `sales-and-inventory-management-system-182200-182209/`, a forwarding `gradlew` and `gradlew.bat` are provided that delegate to `mobile_frontend/gradlew*`.

Before running, ensure permissions:
```
bash /home/kavia/workspace/code-generation/prepare-ci-shims.sh
```

Or run from repo root:
```
bash ./run-mobile-analysis.sh
```
