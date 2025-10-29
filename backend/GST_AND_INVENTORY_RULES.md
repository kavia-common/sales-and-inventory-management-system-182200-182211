GST and Inventory Rules

GST calculation per line item:
- unit_price: the product price or overridden unit_price in request
- line_subtotal = unit_price * qty
- line_gst = line_subtotal * (gst_rate / 100)
- line_total = line_subtotal + line_gst
- Rounding: HALF_UP to 2 decimals

Sale totals:
- subtotal = sum(line_subtotal)
- gst_total = sum(line_gst)
- grand_total = subtotal + gst_total

Inventory adjustments:
- On sale creation: decrement product.stock_qty by qty per line
- Record an InventoryMovement for each line item with change_qty = -qty and reason "Sale #<sale_id>"
- Manual adjustments can be recorded via /inventory/movements with positive (add) or negative (remove) quantities
