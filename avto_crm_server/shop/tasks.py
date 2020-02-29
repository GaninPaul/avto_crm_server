import time
import hashlib
import json
import requests
from .models import Product
from avto_crm_server.avto_crm_server.celery import app


URL = "http://127.0.0.1:16732/requests"
HEADERS = { 'Content-type': 'application/json' }
OPERATOR = {
    'name': 'Ганин Семен Владимирович',
    'vatin': '631215424991'
}


@app.task
def print_sale_check(sale):
    data = '{pk}{method}'.format(pk=sale['id'], method='sell')
    uuid = hashlib.md5(bytes(data, encoding='utf-8')).hexdigest()
    items = [create_item(i) for i in sale['product_list']]
    total_sum = sum(d['amount']*d['quantity'] for d in items)
    json_data = {
        'uuid': uuid,
        'request': [
            {
                'type': 'sell',
                'taxationType': 'envd',
                'ignoreNonFiscalPrintErrors': True,
                'operator': OPERATOR,
                'preItems': [
                    {
                        'type': 'text',
                        'text': "Номер чека {pk}".format(pk=sale['id']),
                        'alignment': 'left'
                    },
                ],
                'items': items,
                'payments': [
                    {
                        'type': 'cash',
                        'sum': total_sum,
                    },
                ],
                'total': total_sum

            }
        ]
    }
    r = requests.post(
        URL,
        data=json.dumps(json_data),
        headers=HEADERS
    )


@app.task
def print_refund_check(sale):
    data = '{pk}{method}'.format(pk=sale['id'], method='sellReturn')
    uuid = hashlib.md5(bytes(data, encoding='utf-8')).hexdigest()
    items = [create_item(i) for i in sale['product_list']]
    total_sum = sum(d['amount'] * d['quantity'] for d in items)
    json_data = {
        'uuid': uuid,
        'request': [
            {
                'type': 'sellReturn',
                'taxationType': 'envd',
                'ignoreNonFiscalPrintErrors': True,
                'operator': OPERATOR,
                'items': items,
                'payments': [
                    {
                        'type': 'cash',
                        'sum': total_sum,
                    },
                ],
                'total': total_sum

            }
        ]
    }
    r = requests.post(
        URL,
        data=json.dumps(json_data),
        headers=HEADERS
    )

@app.task
def open_cashier():
    data = '{time}{method}'.format(time=time.clock(), method='openShift')
    uuid = hashlib.md5(bytes(data, encoding='utf-8')).hexdigest()
    json_data = {
        'uuid': uuid,
        'request': [
            {
                'type': 'openShift',
                'operator': OPERATOR
            }
        ]
    }
    r = requests.post(
        URL,
        data=json.dumps(json_data),
        headers=HEADERS
    )


@app.task
def close_cashier():
    data = '{time}{method}'.format(time=time.clock(), method='closeShift')
    uuid = hashlib.md5(bytes(data, encoding='utf-8')).hexdigest()
    print(uuid)
    json_data = {
        'uuid': uuid,
        'request': [
            {
                'type': 'closeShift',
                'operator': OPERATOR
            }
        ]
    }
    r = requests.post(
        URL,
        data=json.dumps(json_data),
        headers=HEADERS
    )


def create_item(item):
    return {
        "type": "position",
        "name": Product.objects.get(pk=item['product']).name,
        "price": item['price'],
        "quantity": item['count'],
        "amount": item['price']*item['count'],
        "department": 1,
        "measurementUnit": "шт",
        "paymentMethod": "fullPayment",
        "paymentObject": "commodity",
        "tax": {
            "type": "vat0"
        }
    }
