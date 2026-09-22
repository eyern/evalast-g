from django.contrib import admin
from .models import (
    Book,
    Category,
    Order,
    OrderItem,
    CustomerProfile,
    Review,
    Cart,
    CartItem,
    Coupon
)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'category',
        'price',
        'stock',
        'status',
        'show_on_home',
        'home_section',
    )

    search_fields = (
        'title',
        'author',
        'isbn',
        'publisher',
    )

    list_filter = (
        'category',
        'status',
        'show_on_home',
        'home_section',
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'status',
    )

    search_fields = (
        'name',
    )

    list_filter = (
        'status',
    )

class OrderItemInline(admin.TabularInline):

    model = OrderItem

    extra = 0

    readonly_fields = (
        'price',
    )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'customer',
        'total_amount',
        'status',
        'payment_status',
        'created_at',
    )

    search_fields = (
        'id',
        'customer_username',
        'customer_email',
    )

    list_filter = (
        'status',
        'payment_status',
        'created_at',
    )

    ordering = (
        '-created_at',
    )

    inlines = [
        OrderItemInline,
    ]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        'order',
        'book',
        'quantity',
        'price',
        'get_total',
    )

    search_fields = (
        'order__customer__username',
        'book__title',
    )

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'full_name',
        'phone',
        'city',
        'country',
    )

    search_fields = (
        'user__username',
        'user__email',
        'full_name',
        'phone',
    )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        'customer',
        'book',
        'rating',
        'status',
        'created_at',
    )

    search_fields = (
        'customer__username',
        'customer__email',
        'book__title',
        'comment',
    )

    list_filter = (
        'rating',
        'status',
        'created_at',
    )

    ordering = (
        '-created_at',
    )

class CartItemInline(admin.TabularInline):

    model = CartItem

    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'created_at',
        'updated_at',
    )

    search_fields = (
        'user__username',
        'user__email',
    )

    inlines = [
        CartItemInline,
    ]

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):

    list_display = (
        'cart',
        'book',
        'quantity',
        'created_at',
    )

    search_fields = (
        'cart__user__username',
        'book__title',
    )

