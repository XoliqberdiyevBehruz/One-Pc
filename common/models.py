from django.db import models
from django.db.models import CharField
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Advertisement(models.Model):
    image_en = models.FileField(upload_to='media/common/advertisement', null=True)
    image_uz = models.FileField(upload_to='media/common/advertisement', null=True)
    image_ru = models.FileField(upload_to='media/common/advertisement', null=True)
    mb_image_en = models.FileField(upload_to='media/common/advertisement/mb_image', null=True, verbose_name='mobile_image_en')
    mb_image_uz = models.FileField(upload_to='media/common/advertisement/mb_image', null=True, verbose_name='mobile_image_uz')
    mb_image_ru = models.FileField(upload_to='media/common/advertisement/mb_image', null=True, verbose_name='mobile_image_ru')
    link = models.URLField()

    class Meta:
        verbose_name = 'Advertisement'
        verbose_name_plural = 'Advertisements'


class ContactUs(BaseModel):
    name = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=120)
    is_contacted = models.BooleanField(default=False)

    def __str__(self) -> CharField:
        return self.name or self.phone_number

    class Meta:
        verbose_name = _('Contact Us')
        verbose_name_plural = _('Contact Us')
        ordering = ['is_contacted']


class AboutUs(BaseModel):
    title = models.CharField(max_length=120)
    description = models.TextField()
    video = models.FileField(upload_to='common/about-us/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('About Us')
        verbose_name_plural = _('About Us')


class ExcelFile(models.Model):
    file = models.FileField(
        upload_to='excel_file/',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])]    
    )

    class Meta:
        verbose_name = 'Excel File'
        verbose_name_plural = 'Excel File'