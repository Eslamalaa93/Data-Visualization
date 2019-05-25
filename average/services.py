from datetime import datetime
from django.db.models import *
from common.models import *
from . import DLT_weekly_range
from .constants import *


class AverageService:
    def get_dlt_orders_steps_average_chart(self, fields_param):
        if fields_param.get('cutdate__range', 'not') != 'not':
            start_date = datetime.strptime(fields_param['cutdate__range'][0], '%Y-%m-%d').strftime("%d-%m-%Y")
            end_date = datetime.strptime(fields_param['cutdate__range'][1], '%Y-%m-%d').strftime("%d-%m-%Y")
        else:
            start_date = datetime.strptime(str(min_max_date['cutdate__min']), '%Y-%m-%d').strftime("%d-%m-%Y")
            end_date = datetime.strptime(str(min_max_date['cutdate__max']), '%Y-%m-%d').strftime("%d-%m-%Y")

        steps_days_average_list = self.get_steps_days_average(fields_param)
        steps_days_count_list = self.get_steps_days_count(fields_param)
        steps_start_date_average_list = self.get_steps_start_date_average(fields_param)
        chart_json = DLT_weekly_range.generate_json(steps_days_average_list, start_date, end_date,
                                                    steps_start_date_average_list, steps_days_count_list)

        result = {'chart_json': chart_json}

        return result

    def get_steps_days_average(self, fields_param):

        steps_aggregate_func_list = []

        for process_name in process_names:
            steps_aggregate_func_list += [Avg(process_name)]

        order_days_query_set = DltOrderDays.objects.filter(**fields_param).aggregate(
            *steps_aggregate_func_list)

        steps_days_average_list = []
        for process_name in process_names:
            steps_days_average_list += [order_days_query_set[process_name + '__avg']]

        # steps_days_average_list = list(map(lambda x: int(x), steps_days_average_list))

        return steps_days_average_list

    def get_steps_days_count(self, fields_param):

        steps_aggregate_func_list = []

        for process_name in process_names:
            steps_aggregate_func_list += [Count(process_name)]

        order_days_query_set = DltOrderDays.objects.filter(**fields_param).aggregate(
            *steps_aggregate_func_list)

        order_days_query_list = []
        for process_name in process_names:
            order_days_query_list += [order_days_query_set[process_name + '__count']]

        return order_days_query_list

    def get_steps_start_date_average(self, fields_param):
        task_field = {'DLT1a': ['customer_signature'], 'DLT1b1': ['first_lvo'], 'DLT1b2': ['last_lvo'],
                      'DLT1c': ["gad"],
                      'DLT2': ['gold_cr'], 'DLT3a1': ['sio'], 'DLT3a2': ['cso'], 'DLT3b1': ['sio'],
                      'DLT3b2': ['equipment_order'], 'DLT3b3': ['shipment_requested'], 'DLT3b4': ['shipment_date'],
                      'DLT3d': ['cav', 'equipment_delivery'], 'DLT3e': ['install_order'], 'DLT4a': ['install_request'],
                      'DLT4b': ['at_completion']
                      }
        param = {}
        if len(fields_param) > 1:
            for f in fields_param.items():
                if f[0].find('isnull') > -1:
                    is_null_field = 'dltorderdays__' + f[0] if f[0] != 'id__ltc__isnull' else 'ltc__isnull'
                    param[is_null_field] = f[1]
                elif f[0].find('cutdate__range') > -1:
                    param['cutdate__range'] = f[1]
                else:
                    param[f[0].split('__')[1]] = f[1]
        else:
            param = fields_param

        extra_select_columns = {}
        task_field = sorted(task_field.items())

        for field in task_field:
            extra_select_columns[
                'avg_' + field[0] + '_start'] = 'FROM_UNIXTIME(AVG(unix_timestamp(' + field[1][0] + ')))'
            if len(field[1]) > 1:
                extra_select_columns[
                    'avg_' + field[0] + '_start_2'] = 'FROM_UNIXTIME(AVG(unix_timestamp(' + field[1][1] + ')))'

        process_date_averages_query_set = DltOrderDetail.objects.values().extra(select=extra_select_columns) \
            .filter(**param)

        process_date_averages_query_set = process_date_averages_query_set[0]

        if process_date_averages_query_set[
            'avg_DLT3d_start_2'] is not None and process_date_averages_query_set['avg_DLT3d_start'] is not None:
            process_date_averages_query_set['avg_DLT3d_start'] = max(process_date_averages_query_set['avg_DLT3d_start'],
                                                                     process_date_averages_query_set[
                                                                         'avg_DLT3d_start_2'])
        else:
            process_date_averages_query_set['avg_DLT3d_start'] = process_date_averages_query_set['avg_DLT3d_start'] if \
                process_date_averages_query_set['avg_DLT3d_start'] is not None else process_date_averages_query_set[
                'avg_DLT3d_start_2']

        dates_average_list = []
        for field in task_field:
            dates_average_list += [process_date_averages_query_set['avg_' + field[0] + '_start']]

        dates_average_list = dates_average_list[0:len(process_names)]

        return dates_average_list
