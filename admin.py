from django.contrib import admin
from .models import *

# -----------------------------
#  BASIC MODEL REGISTRATION
# -----------------------------
admin.site.register(user)
admin.site.register(Selling)
admin.site.register(UserPurchasedProperty)
admin.site.register(RefundRequest)
admin.site.register(LoginData)


# -----------------------------
# 1️⃣ PROPERTY ADMIN
# -----------------------------
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'location', 'price', 'status', 'seller')
    list_filter = ('status', 'category', 'location')
    search_fields = ('title', 'location', 'seller__username')
    list_per_page = 20
    ordering = ('-id',)


# -----------------------------
# 2️⃣ CATEGORY ADMIN
# -----------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_id', 'amount', 'status', 'created_at')
    search_fields = ('payment_id', 'user__username')

class RefundRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'purchased_property', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'purchased_property__property__title', 'reason')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

class SellingAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'property_type', 'price', 'status', 'is_active')
    list_filter = ('status', 'property_type', 'is_active')
    search_fields = ('title', 'location', 'aadhaar_number')
    ordering = ('-id',)
    actions = ['approve_selling', 'reject_selling']

    def approve_selling(self, request, queryset):
        queryset.update(status='APPROVED')
    approve_selling.short_description = "Approve selected user properties"

    def reject_selling(self, request, queryset):
        queryset.update(status='REJECTED', is_active=False)
    reject_selling.short_description = "Reject selected user properties"