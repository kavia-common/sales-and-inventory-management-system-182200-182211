# Mobile CI Instructions

Some CI jobs attempt to run `./gradlew` from varying working directories.

Use one of these options:
- Run `bash ./bootstrap-mobile-ci.sh` from repo root
- Or call `bash ./gradlew-relay.sh tasks` from any subdirectory; it locates root `./gradlew` shim and executes it.

Shims included:
- `./gradlew` (root)
- `android/gradlew`
- `sales-and-inventory-management-system-182200-182209/mobile_frontend/gradlew`
- `.ci-mobile/gradlew`
- Relay: `gradlew-relay.sh`
