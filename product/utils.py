import requests
import pandas as pd

from product import models
from common.models import ExcelFile


def create_or_update_products():
    # Excel fayldan artikllarni olish
    artickles = []
    excel_file = ExcelFile.objects.first().file
    if excel_file:
        df = pd.read_excel(excel_file.path, dtype=str)
        artickles = df['Artikle'].astype(str).tolist()

    # API dan ma'lumot olish
    url = 'http://195.158.30.91/ONECOMPUTERS/hs/item/getdata'
    response = requests.get(url, auth=('HttpUser', '85!@fdfd$DES35wgf&%'))

    if response.status_code != 200:
        return "API dan ma'lumot olinmadi"

    data = response.json().get("data", [])
    total_created = 0
    total_processed = 0

    # Barcha mahsulotlarni qayta ishlash
    for product in data:
        total_processed += 1
        item = str(product['article'])

        # Excelda mavjud bo‘lmagan artikllarni tashlab ketamiz
        if item not in artickles:
            continue

        price = product.get('price')
        category_name = product.get('category')

        if category_name and category_name.strip():
            category, _ = models.ProductCategory.objects.get_or_create(
                name="".join((category_name.split(". ", 1)[1:]))
            )
        else:
            continue
        
        brand = None
        if product.get('brend'):
            brand, _ = models.ProductBrand.objects.get_or_create(name=product.get('brend'))

        obj, created = models.Product.objects.update_or_create(
            item=item,
            defaults={
                'price': price if price else 0,
                "quantity_left": 0,
                'name': product.get('name'),
                'name_uz': product.get('name'),
                'category': category,
                'brand': brand
            }
        )
        if created:
            total_created += 1

    return f"{total_created} ta mahsulot qo'shildi va {total_processed} ta mahsulot yangilandi"
