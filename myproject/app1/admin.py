
from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Category,
    Product,
    ProductImage,
    Customer,
    Address,
    Cart,
    CartItem,
    Order,
    OrderItem,
    Payment,
    Review,
    Wishlist,
    Coupon,
)


# =====================================
# CATEGORY ADMIN
# =====================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image_preview', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit:cover;" />',
                obj.image.url
            )
        return "No Image"

    image_preview.short_description = 'Category Image'


# =====================================
# PRODUCT IMAGE INLINE
# =====================================

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text')
    verbose_name = 'Product Image'
    verbose_name_plural = 'Product Images'


# =====================================
# PRODUCT ADMIN
# =====================================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'brand',
        'category',
        'price',
        'discount_price',
        'stock',
        'is_available',
        'is_featured',
    )

    search_fields = ('name', 'brand', 'sku')
    list_filter = ('category', 'is_available', 'is_featured')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]


# =====================================
# CUSTOMER ADMIN
# =====================================

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'date_of_birth')
    search_fields = ('user__username', 'phone')


# =====================================
# ADDRESS ADMIN
# =====================================

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer',
        'full_name',
        'city',
        'state',
        'pincode',
    )
    search_fields = ('full_name', 'city', 'pincode')


# =====================================
# CART ADMIN
# =====================================

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'created_at')


# =====================================
# CART ITEM ADMIN
# =====================================

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity')


# =====================================
# ORDER ADMIN
# =====================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number',
        'customer',
        'total_amount',
        'status',
        'ordered_at',
    )
    search_fields = ('order_number', 'customer__user__username')
    list_filter = ('status',)


# =====================================
# ORDER ITEM ADMIN
# =====================================

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price')


# =====================================
# PAYMENT ADMIN
# =====================================

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'payment_method',
        'amount',
        'status',
    )
    list_filter = ('payment_method', 'status')


# =====================================
# REVIEW ADMIN
# =====================================

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer',
        'product',
        'rating',
        'created_at',
    )
    list_filter = ('rating',)


# =====================================
# WISHLIST ADMIN
# =====================================

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer')


# =====================================
# COUPON ADMIN
# =====================================

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'discount_percentage',
        'minimum_amount',
        'valid_from',
        'valid_to',
        'is_active',
    )
    search_fields = ('code',)
    list_filter = ('is_active',)
