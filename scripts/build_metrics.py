#!/usr/bin/env python3
"""Build privacy-safe dashboard data from a Cafe24 order CSV.
No names, phone numbers, addresses, or order IDs are written to the output."""
import csv, json, sys
from collections import defaultdict, Counter
from datetime import datetime
from pathlib import Path

def money(v):
    try: return float((v or '0').replace(',', ''))
    except ValueError: return 0.0

def main(src, dst):
    with open(src, encoding='utf-8-sig', newline='') as f: rows=list(csv.DictReader(f))
    orders={}
    products=defaultdict(lambda:{'qty':0,'sales':0.0,'orders':set()})
    dates=Counter()
    for r in rows:
        oid=r.get('주문번호','')
        if oid not in orders:
            orders[oid]={'paid':money(r.get('총 결제금액')),'order_amount':money(r.get('총 주문금액')),'date':r.get('발주일','')}
        qty=int(float(r.get('수량') or 0))
        name=r.get('주문상품명','')
        products[name]['qty'] += qty
        products[name]['sales'] += money(r.get('판매가'))*qty
        products[name]['orders'].add(oid)
    for o in orders.values():
        raw=(o.get('date') or '')[:10]
        if raw: dates[raw]+=1
    paid=sum(x['paid'] for x in orders.values())
    result={'updated_at':datetime.utcnow().isoformat(timespec='seconds')+'Z','source':'Cafe24 CSV','period':{'from':min(dates) if dates else None,'to':max(dates) if dates else None},'summary':{'csv_rows':len(rows),'orders':len(orders),'paid':round(paid),'order_amount':round(sum(x['order_amount'] for x in orders.values())),'aov':round(paid/len(orders)) if orders else 0,'units':sum(x['qty'] for x in products.values()),'friend_orders':len(orders),'nonfriend_orders':0},'daily':[{'date':d,'orders':n} for d,n in sorted(dates.items())],'products':[{'name':n,'qty':v['qty'],'sales':round(v['sales']),'orders':len(v['orders'])} for n,v in sorted(products.items(),key=lambda kv:-kv[1]['sales'])]}
    Path(dst).parent.mkdir(parents=True,exist_ok=True)
    Path(dst).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: build_metrics.py INPUT.csv OUTPUT.json')
    main(sys.argv[1],sys.argv[2])
