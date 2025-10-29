#!/usr/bin/env pwsh
# PowerShell shim to support CI environments invoking .\gradlew on Windows shells
$ErrorActionPreference = "Stop"
bash "sales-and-inventory-management-system-182200-182209/run_mobile_no_wrapper.sh" $args
