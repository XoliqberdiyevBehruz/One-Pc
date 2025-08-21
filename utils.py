import os
import django
import re

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")  
django.setup()

import requests
import json
from product import models
from openpyxl import load_workbook


def clean_number(price):
    if price:  
        num = re.sub(r"\D", "", str(price))
        return int(num) if num else 0  
    return 0 


file_path = "WEB SAYT.xlsx"
wb = load_workbook(file_path)
sheet = wb.active  

article_list = []
for row in sheet.iter_rows(min_row=2, max_col=2, values_only=True):
    if row[1]:  
        article_list.append(row[1])


url = 'http://195.158.30.91/ONECOMPUTERS/hs/item/getdata'
headers = {'Content-Type': 'application/json'}
payload = {"sap_codes": article_list}

response = requests.post(url, auth=('HttpUser', '85!@fdfd$DES35wgf&%'), headers=headers, data=json.dumps(payload))

if response.status_code == 200:
    data = response.json()
    for product in data["data"]:
        item = product['Товар']
        price = product['Цена']
        remainder = product['Остатка']  
        clean_price = clean_number(str(price))            
        models.Product.objects.update_or_create(
            item=item,
            defaults={
                'price': clean_price,
                "quantity_left": max(0, remainder if remainder else 0)
            }
        )