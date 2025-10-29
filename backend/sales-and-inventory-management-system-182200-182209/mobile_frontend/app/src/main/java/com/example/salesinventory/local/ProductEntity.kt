package com.example.salesinventory.local

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "products")
data class ProductEntity(
    @PrimaryKey val id: Int,
    val name: String,
    val sku: String,
    val price: String,
    val gstRate: String,
    val stockQty: Int
)
