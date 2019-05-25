from datetime import datetime
from datetime import timedelta
import calendar
from common.models import *

PROCESSES_IS_BOLD = '0'

TASK_ESTIMATED_COLOR = '#7a7a7a'

PROCESSES_BGALPHA = '25'

PROCESSES_HEADER_FONT_SIZE = '12'

PROCESSES_HEADER_FONT_COLOR = '#ffffff'

PROCESSES_HEADER_BGCOLOR = '#999999'

PROCESSES_BGCOLOR = '#ffffff'

PROCESSES_FONT_SIZE = '11'

PROCESSES_FONT_COLOR = '#000000'

CATEGORIES_FONT_SIZE = '12'

CATEGORIES_FONT_COLOR = '#ffffff'

CATEGORIES_BGCOLOR = '#999999'

CAPTION_FONT_SIZE = '19'

SLACK_FILL_COLOR = '#e44a00'

GRID_BORDER_ALPHA = '20'

GRID_BORDER_COLOR = '#333333'

TASK_ACTUAL_COLOR = '#f26722'


def is_date(x):
    try:
        datetime.strptime(str(x), '%Y-%m-%d')
        return True
    except ValueError:
        return False


def generate_order_json(order_id):
    order_details = DltOrderDetail.objects.filter(id=order_id).values()

    chart = {'caption': 'Delivery Lead Time Process Visualization', 'subcaption': order_id, 'dateformat': 'dd/mm/yyyy',
             'showFullDataTable': '1', 'ganttpanedurationunit': 'm', 'ganttwidthpercent': '60',
             'legendborderalpha': '30',
             'legendshadow': '0', 'useplotgradientcolor': '0', 'showcanvasborder': '0',
             'gridbordercolor': GRID_BORDER_COLOR, 'gridborderalpha': GRID_BORDER_ALPHA,
             'slackfillcolor': SLACK_FILL_COLOR,
             'taskbarfillmix': 'light+0', 'categoryHoverBandAlpha': '50', 'categoryHoverBandColor': '#cccccc',
             'showTaskLabels': '0', 'forceRowHeight': '1', 'captionFontSize': CAPTION_FONT_SIZE, 'captionFontBold': '1',
             'legendCaption': 'Coloring Description'}

    categories = {'bgcolor': CATEGORIES_BGCOLOR, 'align': 'middle', 'fontcolor': CATEGORIES_FONT_COLOR,
                  'fontsize': CATEGORIES_FONT_SIZE}

    min_date = datetime(year=2022, month=1, day=1).date()
    max_date = datetime(year=1900, month=1, day=1).date()

    record_field = {}
    for field, value in order_details[0].items():
        record_field[field] = ''
        if is_date(value):
            record_field[field] = datetime.strptime(str(value), '%Y-%m-%d')
            min_date = min(min_date, value)
            max_date = max(max_date, value)

    min_date = (datetime.combine(min_date, datetime.min.time()) - timedelta(days=10)).date()
    max_date = (datetime.combine(max_date, datetime.min.time()) + timedelta(days=15)).date()
    category = []
    while min_date <= max_date:
        temp_category = {'start': min_date.strftime('%d/%m/%Y')}
        endOfMonth = calendar.monthrange(min_date.year, min_date.month)[1]
        temp_category['end'] = datetime(year=min_date.year, month=min_date.month, day=endOfMonth).date().strftime(
            '%d/%m/%Y')
        temp_category['label'] = str(min_date.strftime('%B'))
        category.append(temp_category)
        if min_date.month >= 12:
            min_date = datetime(min_date.year + 1, 1, 1).date()
        else:
            min_date = datetime(min_date.year, min_date.month + 1, 1).date()

    categories['category'] = category
    chart['ganttpaneduration'] = str(len(category) - 1)

    processes = {'headertext': 'Process Name', 'fontcolor': PROCESSES_FONT_COLOR, 'fontsize': PROCESSES_FONT_SIZE,
                 'isanimated': '1', 'bgcolor': PROCESSES_BGCOLOR, 'headervalign': 'bottom', 'headeralign': 'left',
                 'headerbgcolor': PROCESSES_HEADER_BGCOLOR, 'headerfontcolor': PROCESSES_HEADER_FONT_COLOR,
                 'headerfontsize': PROCESSES_HEADER_FONT_SIZE, 'align': 'left', 'isbold': PROCESSES_IS_BOLD,
                 'bgalpha': PROCESSES_BGALPHA}

    dlt_process = ["DLT1a (CSD to 1st LVO)", "DLT1b1 (1st LVO to Last LVO)", "DLT1b2 (Last LVO to GAD)",
                   "DLT1c (GAD to SIO)", "DLT2 (C&amp;R to SRF2)", "DLT3a1 (SIO to CCT ORD)", "DLT3a2 (CCT ORD to CAV)",
                   "DLT3b1 (SIO to EQ ORD)", "DLT3b2 (EQ ORD to SHIP Req)", "DLT3b3 (SHIP Req to SHIP)",
                   "DLT3b4 (SHIP to EQ DLV)", "DLT3d (CAV/EQ DLV to FE Req)", "DLT3e (FE Req to 1st INST Req)",
                   "DLT4a (1st INST Req to AT)", "DLT4b (AT to SAT)"]
    process = []
    for i in range(len(dlt_process)):
        temp_process = {'id': str(i + 1), 'label': str(dlt_process[i])}
        process.append(temp_process)

    processes['process'] = process

    task = []
    task_field = {'DLT1a': ['3', ['customer_signature'], ['first_lvo']], 'DLT1b1': ['2', ['first_lvo'], ['last_lvo']],
                  'DLT1b2': ['2', ['last_lvo'], ["gad"]], 'DLT1c': ['2', ["gad"], ["sio"]],
                  'DLT2': ['10', ['gold_cr'], ['srf']],
                  'DLT3a1': ['4', ['sio'], ['cso']], 'DLT3a2': ['55', ['cso'], ['cav']],
                  'DLT3b1': ['10', ['sio'], ['equipment_order']],
                  'DLT3b2': ['25', ['equipment_order'], ['shipment_requested']],
                  'DLT3b3': ['5', ['shipment_requested'], ['shipment_date']],
                  'DLT3b4': ['5', ['shipment_date'], ['equipment_delivery']],
                  'DLT3d': ['7', ['cav', 'equipment_delivery'], ['install_order']],
                  'DLT3e': ['5', ['install_order'], ['install_request']],
                  'DLT4a': ['10', ['install_request'], ['at_completion', 'actual_install']],
                  'DLT4b': ['1', ['at_completion'], ['sat_completion']]
                  }

    def max_date(d1, d2):
        if d1 != '' and d2 != '':
            return max(d1, d2)
        return d1 if (d2 == '') else d2

    def estimate_task(est_task):
        dlt_name = est_task[0]
        val = est_task[1]
        estimated_task = {'label': 'Estimated_' + str(dlt_name) + ' -  ' + val[0] + ' days', 'processid': str(indx),
                          'color': TASK_ESTIMATED_COLOR, 'height': '15%', 'toppadding': '25%'}
        if len(val[1]) > 1:
            s_date = max_date(record_field[val[1][0]], record_field[val[1][1]])
        else:
            s_date = record_field[val[1][0]]

        if s_date != '':
            estimated_task['start'] = s_date.strftime('%d/%m/%Y')
            estimated_task['end'] = (s_date + timedelta(days=int(val[0]))).strftime('%d/%m/%Y')
            return estimated_task
        else:
            return ''
            # task.append(estimated_task)

    def actual_task(act_task):
        dlt_name = act_task[0]
        start_val = act_task[1][1]
        end_val = act_task[1][2]
        s_date = record_field[start_val[0]] if len(start_val) == 1 else max_date(record_field[start_val[0]],
                                                                                 record_field[start_val[1]])
        e_date = record_field[end_val[0]] if len(end_val) == 1 else max_date(record_field[end_val[0]],
                                                                             record_field[end_val[1]])
        if s_date != '' and e_date != '' and s_date <= e_date:
            num_days = '-1' if s_date > e_date else str((e_date - s_date).days)
            num_days = '-1' if int(num_days) > 1000 else num_days
            actual = {'label': 'Actual_' + str(dlt_name) + ' -  ' + num_days + ' days', 'processid': str(indx),
                      'height': '32%', 'toppadding': '56%', 'start': s_date.strftime('%d/%m/%Y'),
                      'end': e_date.strftime('%d/%m/%Y'), 'color': '#ff2626' if num_days == '-1' else TASK_ACTUAL_COLOR}
            # task.append(actual)
            return actual
        else:
            return ''

    indx = 1
    task_field = sorted(task_field.items())
    for field in task_field:
        estimated = estimate_task(field)
        actual = actual_task(field)
        if estimated != '' and actual != '':
            task.append(estimated)
            task.append(actual)
        indx += 1

    tasks = {'task': task}
    items = []
    item = {'label': 'Actual', 'color': TASK_ACTUAL_COLOR}
    items.append(item)
    item = {'label': 'Estimated', 'color': TASK_ESTIMATED_COLOR}
    items.append(item)
    legend = {'item': items}
    gantt_chart = {'chart': chart, 'categories': [categories], 'processes': processes, 'tasks': tasks, 'legend': legend}
    return gantt_chart
