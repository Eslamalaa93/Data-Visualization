from django.db.models import *
from common.models import *

process_names = ['dlt1a', 'dlt1b1', 'dlt1b2', 'dlt1c', 'dlt2', 'dlt3a1', 'dlt3a2', 'dlt3b1', 'dlt3b2',
                 'dlt3b3', 'dlt3b4', 'dlt3d', 'dlt3e', 'dlt4a', 'dlt4b']

min_max_date = DltOrderDetail.objects.aggregate(Max('cutdate'), Min('cutdate'))

