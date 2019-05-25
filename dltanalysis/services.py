from common.models import *
from django.db.models import *
from datetime import *
from operator import itemgetter


def dlt_analysis_service(data_fields):
    fields_param = build_query_fields(data_fields)
    impact = dlt_analysis(fields_param)
    return impact


def dlt_analysis(fields_param):
    field = sorted(fields_param)
    dlt = field[1].split('__')[0]
    per = field[2].split('__is')[0]

    data = DltOrderDays.objects.filter(**fields_param).values(str(per)).annotate(
        volume=Count('id'), dlt=Avg(str(dlt))).filter(dlt__gt='-1')

    product_sum = 0
    total_orders = 0

    for cust in data:
        product_sum += (cust['volume'] * cust['dlt'])
        total_orders += cust['volume']

    if total_orders > 0:
        product_sum /= total_orders

    impact = []
    for cust in data:
        dic = {per: cust[per], 'volume': cust['volume'], dlt: int(cust['dlt']), 'impact': (product_sum - (
            ((total_orders * product_sum) - (cust['volume'] * cust['dlt'])) / (
                total_orders - cust['volume'])))}
        impact.append(dic)

    impact = sorted(impact, key=itemgetter('impact'), reverse=True)

    return impact


def build_query_fields(data_fields):
    field_param = {}
    start_date = datetime.strptime(data_fields['date']['start_date'], '%d-%m-%Y').date()
    end_date = datetime.strptime(data_fields['date']['end_date'], '%d-%m-%Y').date()

    field_param['cutdate__range'] = [str(start_date), str(end_date)]
    field_param[data_fields['Dlt'].lower() + '__isnull'] = False
    field_param['id__' + data_fields['Per'] + '__isnull'] = False
    print(field_param)
    return field_param
