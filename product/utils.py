import requests
from concurrent.futures import ProcessPoolExecutor
from django.db import transaction
from product import models


def process_chunk(chunk):
    """Bitta bo‘lakdagi mahsulotlarni DB ga yozish."""
    created_count = 0
    count = 0

    for product in chunk:
        count += 1
        item = product['article']
        price = product['price']
        category_name = product['category']

        if category_name or category_name != "":
            category, _ = models.ProductCategory.objects.get_or_create(
                name="".join((category_name.split(". ", 1)[1:]))
            )
        else:
            category, _ = models.ProductCategory.objects.get_or_create(name='Boshqa')

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
            created_count += 1

    return created_count, count


def create_or_update_products():
    url = 'http://195.158.30.91/ONECOMPUTERS/hs/item/getdata'
    response = requests.get(url, auth=('HttpUser', '85!@fdfd$DES35wgf&%'))

    if response.status_code != 200:
        return "API dan ma'lumot olinmadi"

    data = response.json().get("data", [])
    total_count = len(data)

    # Ma’lumotni 4 ta bo‘lakka bo‘lamiz (CPU core soniga qarab oshirish mumkin)
    chunk_size = max(1, total_count // 4)
    chunks = [data[i:i + chunk_size] for i in range(0, total_count, chunk_size)]

    total_created = 0
    total_processed = 0

    # Parallel ishlatamiz
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = executor.map(process_chunk, chunks)

    # Natijalarni yig‘amiz
    for created_count, count in results:
        total_created += created_count
        total_processed += count

    return f"{total_created}ta maxsulot qoshildi va {total_processed}ta maxsulot yangilandi"
