import uuid

from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel

DELIVERY, TAKE_AWAY = (_('yetkazib berish'), _('olib ketish'))
NEW_ORDER, IN_PROCESS, CANCELLED, FINISHED = ('yangi buyurtma', 'jarayonda', 'bekor qiligan', 'tugatilgan')


class ProductCategory(BaseModel):
    icon = models.ImageField(upload_to='product/category/', null=True, blank=True)
    name = models.CharField(max_length=250)
    is_popular = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('product category')
        verbose_name_plural = _('product categories')


class ProductBrand(BaseModel):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('product brand')
        verbose_name_plural = _('product brands')


class ProductColor(BaseModel):
    rgba_name = models.CharField(max_length=250)
    name = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.name or self.rgba_name

    class Meta:
        verbose_name = _('product color')
        verbose_name_plural = _('product colors')


class TechnicalInformation(BaseModel):
    name = models.CharField(max_length=250)
    category = models.ManyToManyField(ProductCategory, related_name='tec_infos')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('technical information')
        verbose_name_plural = _('technical information')


class TecInfoName(BaseModel):
    name = models.CharField(max_length=250)
    tec_info = models.ForeignKey(TechnicalInformation, on_delete=models.CASCADE, related_name='tec_infos')

    def __str__(self):
        return f'{self.name} - {self.tec_info.name}'

    class Meta:
        verbose_name = _('tec info name')
        verbose_name_plural = _('tec info names')


class ProductTecInfo(BaseModel):
    tec_info = models.ForeignKey(TechnicalInformation, on_delete=models.CASCADE, related_name='product_tec_infos')
    tec_info_name = models.ForeignKey(TecInfoName, on_delete=models.CASCADE, related_name='product_tec_infos')

    def save(self, *args, **kwargs):
        if self.tec_info_name.tec_info == self.tec_info:
            super(ProductTecInfo, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.tec_info.name} - {self.tec_info_name.name}'

    class Meta:
        verbose_name = _('product tec info')
        verbose_name_plural = _('product tec infos')
        unique_together = ('tec_info', 'tec_info_name')


class Product(BaseModel):
    name = models.CharField(max_length=250, null=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)
    main_image = models.ImageField(upload_to='product/product/', null=True, blank=True)
    brand = models.ForeignKey(ProductBrand, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)
    price = models.PositiveBigIntegerField(default=0)
    quantity_left = models.PositiveIntegerField(default=0, null=True, blank=True)
    item = models.CharField(max_length=250, unique=True)
    discount_percentage = models.PositiveIntegerField(default=0)
    is_discount = models.BooleanField(default=False)
    is_top = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    info = models.ManyToManyField(ProductTecInfo, null=True, blank=True, related_name='products')
    colors = models.ManyToManyField('ProductColor', null=True, blank=True, related_name='products')

    def __str__(self):
        return self.item

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')


class ProductMedia(BaseModel):
    media = models.FileField(null=True, blank=True, upload_to='product/product-media')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_medias')

    def __str__(self):
        return self.media.name

    class Meta:
        verbose_name = _('product media')
        verbose_name_plural = _('product medias')


class DiscountProduct(BaseModel):
    image_uz = models.ImageField(upload_to='product/discount-product', null=True)
    image_en = models.ImageField(upload_to='product/discount-product', null=True)
    image_ru = models.ImageField(upload_to='product/discount-product', null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = _('discount product')
        verbose_name_plural = _('discount products')


class PopularProduct(BaseModel):
    title = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    banner = models.ImageField(upload_to='product/popular-product')
    description = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('popular product')
        verbose_name_plural = _('popular products')


class Region(BaseModel):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('region')
        verbose_name_plural = _('regions')


class City(BaseModel):
    name = models.CharField(max_length=250)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('city')
        verbose_name_plural = _('cities')


class OrderProductItem(models.Model):
    order = models.ForeignKey('OrderProduct', on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product} - {self.count}'

    class Meta:
        verbose_name = _("order product item")
        verbose_name_plural = _("order product items")


class OrderProduct(BaseModel):
    METHOD = (
        (DELIVERY, DELIVERY),
        (TAKE_AWAY, TAKE_AWAY)
    )
    STATUS = (
        (NEW_ORDER, NEW_ORDER),
        (IN_PROCESS, IN_PROCESS),
        (CANCELLED, CANCELLED),
        (FINISHED, FINISHED),
    )
    status = models.CharField(max_length=250, choices=STATUS)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    method_for_reception = models.CharField(max_length=250, choices=METHOD)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='order_products')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='order_products')
    address = models.CharField(max_length=250)
    floor = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=15,validators=[RegexValidator(regex=r"^(?:\+998|998)?[0-9]{9}$",message="Telefon raqami noto'g'ri formatda. To'g'ri format +998901234567 bo'lishi kerak.",code='invalid_phone_number')])
    comment = models.TextField(null=True, blank=True)
    products = models.ManyToManyField(Product, related_name='order_products', through=OrderProductItem)
    product_count = models.PositiveIntegerField(default=0)
    total_price = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f"{self.first_name} - order"

    class Meta:
        verbose_name = _('order product')
        verbose_name_plural = _('order products')

    @classmethod
    def get_method_for_reception_list(cls):
        return [choice[1] for choice in cls.METHOD]
