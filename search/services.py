from common.models import *
from common.serializers import *
from search.constant import *
from datetime import *


def get_order_details(search_fields):
    order_detail = DltOrderDays.objects.filter(**search_fields).order_by('id').values(*fieldname)
    print(len(order_detail))
    return order_detail


def check_field_data(request_data):
    for key in request_data.keys():
        if key not in process_names:
            return True

    return False


def build_model_query(request_data):
    field = {}
    dates = {}
    for key, value in request_data.items():
        if key == 'end_date' or key == 'start_date':
            date_val = datetime.strptime(value,'%Y-%m-%d').date()
            dates[key] = str(date_val)
        else:
            field['id__' + key + '__icontains'] = value

    if len(dates) is not 0:
        date_field = {}
        date_field["id__cutdate__range"] = [str(dates["start_date"]), str(dates["end_date"])]
        field.update(date_field)

    field["id__num_fields__gt"] = '23'
    print(field)
    return field
