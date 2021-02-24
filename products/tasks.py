import json
import http.client

from celery import shared_task
from django.core.mail import send_mail, mail_admins
from django.template import loader
from django.conf import settings
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def get_stocks(list_ids_or_sku):
    payload1 = {"idType":"sku","idList":list_ids_or_sku}
    payload = str(payload1)
    conn = http.client.HTTPSConnection("ecomdash.azure-api.net")
    headers = {
    'Ocp-Apim-Subscription-Key': 'ce0057d8843342c8b3bb5e8feb0664ac',
    'ecd-subscription-key': '0e26a6d3e46145d5b7dd00a9f0e23c39',
    'Content-Type': 'application/json',
    'Authorization': 'Token 201105f43f33e2b5b287c55cd73823e0d050f537'
    }
    conn.request("POST", "/api/inventory/getProducts", payload, headers)
    res = conn.getresponse()
    data = res.read()
    
    veri = json.loads(data.decode("utf-8"))
    veri2 = veri["data"]
    stocks = []
    id_or_sku_qty_zero = []
    for i in veri["data"]:
        
        stocks.append(i['QuantityOnHand'])
        if int(i['QuantityOnHand']) == 0:
            
            try:
                id_or_sku_qty_zero.append(i["Id"])
            except:
                id_or_sku_qty_zero.append(i["Sku"])
    return [id_or_sku_qty_zero,stocks,veri2]
    