from common.models import *
from datetime import *
from django.db.models import *
from operator import itemgetter
from django.db.models import Subquery


def dlt_target():
    dlt_target = [{'dlt1a__lte': '3', 'dlt1a__isnull': False}, {'dlt1b1__lte': '2', 'dlt1b1__isnull': False},
                  {'dlt1b2__lte': '2', 'dlt1b2__isnull': False}, {'dlt1c__lte': '2', 'dlt1c__isnull': False},
                  {'dlt2__lte': '10', 'dlt2__isnull': False}, {'dlt3a1__lte': '4', 'dlt3a1__isnull': False},
                  {'dlt3a2__lte': '55', 'dlt3a2__isnull': False}, {'dlt3b1__lte': '10', 'dlt3b1__isnull': False},
                  {'dlt3b2__lte': '25', 'dlt3b2__isnull': False}, {'dlt3b3__lte': '5', 'dlt3b3__isnull': False},
                  {'dlt3b4__lte': '5', 'dlt3b4__isnull': False}, {'dlt3d__lte': '7', 'dlt3d__isnull': False},
                  {'dlt3e__lte': '5', 'dlt3e__isnull': False}, {'dlt4a__lte': '10', 'dlt4a__isnull': False},
                  {'dlt4b__lte': '1', 'dlt4b__isnull': False}]

    dlt_name = ['DLT1a', 'DLT1b1', 'DLT1b2', 'DLT1c', 'DLT2', 'DLT3a1', 'DLT3a2', 'DLT3b1', 'DLT3b2', 'DLT3b3',
                'DLT3b4', 'DLT3d', 'DLT3e', 'DLT4a', 'DLT4b']
    dlt_met_target = {}
    indx = 0
    for dlt in dlt_target:
        n_dlt = tuple(dlt.items())[0] if tuple(dlt.items())[0][0].find('lte') > -1 else tuple(dlt.items())[1]
        all_dlt = tuple(dlt.items())[0] if tuple(dlt.items())[0][0].find('isnull') > -1 else tuple(dlt.items())[1]
        dlt_met_target[dlt_name[indx]] = int(
            (DltOrderDays.objects.filter(n_dlt).count() / DltOrderDays.objects.filter(all_dlt).count()) * 100)
        indx += 1

    return dlt_met_target


def top_customer():
    data = DltOrderDetail.objects.filter(customername__isnull=False, ltc__isnull=False).values('customername').annotate(
        volume=Count('id'), ltc=Avg('ltc')).filter(ltc__gt='-1')

    product_sum = 0
    total_orders = 0

    for cust in data:
        product_sum += (cust['volume'] * cust['ltc'])
        total_orders += cust['volume']

    product_sum /= total_orders
    impact = []
    for cust in data:
        dic = cust
        dic['ltc'] = int(dic['ltc'])
        dic['impact'] = (product_sum - (
            ((total_orders * product_sum) - (cust['volume'] * cust['ltc'])) / (
                total_orders - cust['volume'])))
        impact.append(dic)

    impact = sorted(impact, key=itemgetter('impact'), reverse=True)

    return impact[:10]


def top_country():
    data = DltOrderDays.objects.filter(id__country__isnull=False, dlt3a2__isnull=False).values('id__country').annotate(
        volume=Count('id'), dlt3a2=Avg('dlt3a2')).filter(dlt3a2__gt='-1')

    product_sum = 0
    total_orders = 0

    for cust in data:
        product_sum += (cust['volume'] * cust['dlt3a2'])
        total_orders += cust['volume']

    product_sum /= total_orders
    impact = []
    for cust in data:
        dic = cust
        dic['dlt3a2'] = int(dic['dlt3a2'])
        dic['impact'] = (product_sum - (
            ((total_orders * product_sum) - (cust['volume'] * cust['dlt3a2'])) / (
                total_orders - cust['volume'])))
        impact.append(dic)

    impact = sorted(impact, key=itemgetter('impact'), reverse=True)

    return impact[:5]
