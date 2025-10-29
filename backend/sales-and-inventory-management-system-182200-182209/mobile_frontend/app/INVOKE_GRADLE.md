From this directory, you can run Gradle without the wrapper using:
- bash ../run_without_wrapper.sh :app:test

If your CI insists on ./gradlew:
- chmod +x ./gradlew
- ./gradlew :app:test

Wrapper properties are provided at app/gradle/wrapper/gradle-wrapper.properties to assist CI scanners.
