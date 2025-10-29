pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "WorkspaceRootKts"
include(":mobile_frontend_app")
project(":mobile_frontend_app").projectDir = file("sales-and-inventory-management-system-182200-182209/mobile_frontend/app")
