from django.db.models.signals import post_save
from django.dispatch import receiver

from common.models import ExcelFile
from product.utils import create_or_update_products


@receiver(post_save, sender=ExcelFile)
def create_products(sender, **kwargs):
    create_or_update_products()
    