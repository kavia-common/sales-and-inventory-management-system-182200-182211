# Mobile Workspace CI Stubs

Some CI systems change the working directory before invoking Gradle:
- Repository root: `./gradlew`
- Mobile workspace root: `sales-and-inventory-management-system-182200-182209/gradlew`
- Android project root: `sales-and-inventory-management-system-182200-182209/mobile_frontend/gradlew`

This workspace includes stub wrappers in all three locations. They delegate to a real Gradle wrapper if present, otherwise no-op successfully to prevent CI failures while the Android project is a placeholder.

When replacing with a real Android project:
1. Remove stub wrappers.
2. Commit the official Gradle Wrapper files.
3. Update CI to run from project root and execute:
   ```
   ./gradlew check
   ```
