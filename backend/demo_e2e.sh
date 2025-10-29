#!/usr/bin/env bash
set -euo pipefail
# Simple end-to-end demo using curl against a running backend on port 3001
base="http://localhost:3001"
echo "[demo] Health:" && curl -s "$base/health" && echo
echo "[demo] Seed:" && curl -s -X POST "$base/seed" && echo
echo "[demo] Products:" && curl -s "$base/products" && echo
echo "[demo] Create sale:" && curl -s -X POST "$base/sales" -H "Content-Type: application/json" \
  -d '{"customer_name":"Demo Customer","line_items":[{"product_id":1,"qty":2}]}' && echo
echo "[demo] Sales list:" && curl -s "$base/sales" && echo
echo "[demo] Create invoice:" && curl -s -X POST "$base/invoices" -H "Content-Type: application/json" \
  -d '{"sale_id":1,"invoice_number":"INV-1001","billing_address":"123 Street","gstin":"22ABCDE1234F1Z5"}' && echo
echo "[demo] Invoices list:" && curl -s "$base/invoices" && echo
