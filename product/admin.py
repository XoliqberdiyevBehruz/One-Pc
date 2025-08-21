from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import redirect

from modeltranslation.admin import TranslationAdmin, TranslationStackedInline

from product import models, forms
from product.utils import create_or_update_products


class ProductMediasInline(admin.StackedInline):
    model = models.ProductMedia
    extra = 0
    fields = ['media']


class TecInfoNameAdmin(admin.StackedInline):
    model = models.TecInfoName
    extra = 0
    fields = ['name']


class CityInline(TranslationStackedInline):
    model = models.City
    extra = 0
    fields = ['name']


class OrderItemInline(admin.StackedInline):
    model = models.OrderProductItem
    extra = 0
    fields = ['product', 'count']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj):
        return False


@admin.register(models.TechnicalInformation)
class TecInfoAdmin(admin.ModelAdmin):
    inlines = [TecInfoNameAdmin]


@admin.register(models.Product)
class ProductAdmin(TranslationAdmin):
    fieldsets = (
        ('Product Info', {"fields": ("main_image", 'info', 'colors', "category", "brand", 'price', 'discount_percentage', 'is_top', 'is_discount', 'is_popular', 'item', 'quantity_left',)}),
        ("Product Name", {"fields": ("name_uz", "name_ru", "name_en")}),
    )
    inlines = [ProductMediasInline]
    list_display = ['item', 'name_uz', 'name_ru', 'name_en', 'category', 'main_image']
    list_editable = ['name_uz', 'name_ru', 'name_en', 'category', 'main_image']
    search_fields = ('item', 'name_uz', 'name_ru', 'name_en')
    list_filter = ['category'] 
    actions = ['delete_all']
    change_list_template = "admin/custom_changelist.html"

    @admin.action(description="Delete all products")
    def delete_all(self, request, queryset):
        models.Product.objects.all().delete()
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('admin/product/product/', self.update_data, name='update_data'),
        ]
        return custom_urls + urls

    def update_data(self, request):
        res = create_or_update_products()
        messages.success(request, res)
        return redirect("admin:product_product_changelist")  


@admin.register(models.ProductCategory)
class ProductCategoryAdmin(TranslationAdmin):
    list_display = ['name', 'is_popular', 'products_count']
    list_display_links = list_display
    list_filter = ['is_popular']


    def products_count(self, obj):
        return obj.products.count()



@admin.register(models.DiscountProduct)
class DiscountProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_uz', 'product']


@admin.register(models.PopularProduct)
class PopularProductAdmin(TranslationAdmin):
    fieldsets = (
        ('Banner', {"fields": ('banner', 'product')}),
        ("Uzbek tilida", {"fields": ("title_uz", "name_uz", "description_uz")}),
        ("Rus tilida", {"fields": ("title_ru", "name_ru", "description_ru")}),
        ("Ingliz tilida", {"fields": ("title_en", "name_en", "description_en")}),
    )
    list_display = ['name', 'title']
    list_display_links = list_display


@admin.register(models.ProductTecInfo)
class ProductTecInfoAdmin(admin.ModelAdmin):
    form = forms.ProductTecInfoForm


# @admin.register(models.ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    pass


# @admin.register(models.OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    fieldsets = (
        ('User info', {"fields": ('first_name', 'last_name', 'phone_number')}),
        ("Location", {"fields": ("region", "city", "address", 'floor')}),
        ("Order info", {"fields": ("product_count", "total_price", 'comment')}),
        ("Status", {"fields": ("status", "method_for_reception")}),
    )
    filter_horizontal = ('products',)
    inlines = [OrderItemInline]
    # readonly_fields = [
    #     'region', 'city', 'address', 'floor', 'products', 'product_count', 'total_price',
    #     'comment', 'first_name', 'last_name', 'phone_number', 'user',
    # ]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return True


# @admin.register(models.Region)
class RegionAdmin(TranslationAdmin):
    inlines = [CityInline]



@admin.register(models.ProductBrand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = list_display