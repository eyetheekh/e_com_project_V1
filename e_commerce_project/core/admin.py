from django.contrib import admin

from .models import Category, Product, Vendor, Product_Images, Product_Review, Address, Order, CartOrderItems, Contact_Us


class ProductImagesAdmin(admin.TabularInline):
    model = Product_Images


class Product_Admin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['title', 'category', 'vendor', 'price', 'discount_amount', 'tags',
                    'product_status', 'featured_on_home_page',]
    list_editable = ['category', 'vendor', 'product_status', 'price',
                     'discount_amount', 'tags', 'featured_on_home_page',]


class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'default_address']


class contact_us_Admin(admin.ModelAdmin):
    list_display = ['name', 'email', 'message', 'status']

    list_editable = ['status']


admin.site.register(Product, Product_Admin)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(CartOrderItems)
admin.site.register(Vendor)
admin.site.register(Product_Images)
admin.site.register(Product_Review)
admin.site.register(Address, AddressAdmin)
admin.site.register(Contact_Us, contact_us_Admin)
