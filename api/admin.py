from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.safestring import mark_safe

from .models import *
from .forms import UsersCreationForm, UsersChangeForm


class ImageInline(GenericTabularInline):
    model = Images
    extra = 1
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        print(obj.images)
        if obj.images:
            return mark_safe(f'<img src="{obj.images.url}" width="300" height="300" style="object-fit:contain"/>')
        else:
            return '(No image)'

    image_preview.short_description = 'Preview'


class ModelsWithImageAndIdAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]
    readonly_fields = ('quantity_of_goods', 'id')


class SliderAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]
    readonly_fields = ('id',)
    filter_horizontal = ('products',)


class BasketAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


class OrdersAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('id', 'status', 'customers', 'delivery_method', 'payment_method')
    list_filter = ('status', 'delivery_method', 'payment_method')


class CustomUserAdmin(UserAdmin):
    add_form = UsersCreationForm
    form = UsersChangeForm
    model = Users
    list_display = ('email', 'username', 'ip_address', 'status', 'discount', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('email', 'username',  'status', 'discount', 'is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password', 'ip_address', 'status', 'discount', 'first_name', 'last_name')}),
        ('Разрешения', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    readonly_fields = ('id',)


admin.site.register(Categories, ModelsWithImageAndIdAdmin)
admin.site.register(Manufacturers, ModelsWithImageAndIdAdmin)
admin.site.register(Products, ModelsWithImageAndIdAdmin)
admin.site.register(Users, CustomUserAdmin)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(Images)
admin.site.register(Basket, BasketAdmin)
admin.site.register(Slider, SliderAdmin)
