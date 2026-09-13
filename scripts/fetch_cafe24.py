#!/usr/bin/env python3
"""Cafe24 fetch adapter. Store OAuth values only as GitHub Actions secrets."""
import json, os, urllib.parse, urllib.request
from datetime import date, timedelta
from pathlib import Path
mall=os.environ['CAFE24_MALL_ID']
token=os.environ['CAFE24_ACCESS_TOKEN']
base=f'https://{mall}.cafe24api.com/api/v2/admin/orders'
params=urllib.parse.urlencode({'start_date':(date.today()-timedelta(days=90)).isoformat(),'end_date':date.today().isoformat(),'limit':100,'embed':'items'})
req=urllib.request.Request(base+'?'+params,headers={'Authorization':'Bearer '+token,'Content-Type':'application/json'})
with urllib.request.urlopen(req,timeout=30) as r: payload=json.load(r)
# Convert the API response into the same internal shape as the supplied CSV.
# Customer fields are deliberately not written.
import csv
orders=payload.get('orders', payload.get('data', {}).get('orders', []))
Path('private').mkdir(exist_ok=True)
with open('private/orders.csv','w',encoding='utf-8-sig',newline='') as f:
    fields=['주문번호','총 주문금액','총 결제금액','주문상품명','수량','판매가','발주일']
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
    for o in orders:
        oid=str(o.get('order_id',o.get('order_no','')))
        items=o.get('items',o.get('order_items',[])) or [{}]
        for item in items:
            qty=int(float(item.get('quantity',item.get('order_quantity',1)) or 1))
            price=item.get('product_price',item.get('price',o.get('order_price_amount',0))) or 0
            w.writerow({'주문번호':oid,'총 주문금액':o.get('order_price_amount',0),'총 결제금액':o.get('payment_amount',o.get('order_price_amount',0)),'주문상품명':item.get('product_name',item.get('product_name_default','상품')),'수량':qty,'판매가':price,'발주일':o.get('order_date','')})
