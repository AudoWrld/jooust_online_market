# Products admin
from django.contrib import admin
from .models import Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "selling_price", "discount_price", "quantity"]
    list_filter = ["user"]
    search_fields = ["name", "description", "user__email"]
    inlines = [ProductImageInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["product", "image"]
