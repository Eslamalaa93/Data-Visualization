from datetime import datetime
from datetime import timedelta
import calendar

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


def date_format(inputdate):
    if type(inputdate) is str:
        return ''
    if inputdate.year < 2000:
        return ''
    return inputdate.strftime('%d/%m/%Y')


def generate_json(values, from_date, to_date, dates_list, count_per_step):
    chart = {'caption': 'Delivery Lead Time Process Visualization',
             'subcaption': 'from ' + str(from_date) + ' to ' + str(to_date),
             'dateformat': 'dd/mm/yyyy',
             'showFullDataTable': '1', 'ganttpanedurationunit': 'm', 'ganttwidthpercent': '60',
             'legendborderalpha': '30',
             'legendshadow': '0', 'useplotgradientcolor': '0', 'showcanvasborder': '0',
             'gridbordercolor': GRID_BORDER_COLOR, 'gridborderalpha': GRID_BORDER_ALPHA,
             'slackfillcolor': SLACK_FILL_COLOR,
             'taskbarfillmix': 'light+0', 'categoryHoverBandAlpha': '50', 'categoryHoverBandColor': '#cccccc',
             'showTaskLabels': '0', 'forceRowHeight': '1', 'captionFontSize': CAPTION_FONT_SIZE, 'captionFontBold': '1',
             'legendCaption': 'Coloring Description'}

    for i in range(len(values)):
        if values[i] is None:
            values[i] = -1
        else:
            values[i] = int(values[i])

    categories = {'bgcolor': CATEGORIES_BGCOLOR, 'align': 'middle', 'fontcolor': CATEGORIES_FONT_COLOR,
                  'fontsize': CATEGORIES_FONT_SIZE}
    min_date = datetime(year=2022, month=1, day=1)
    max_date = datetime(year=1900, month=1, day=1)

    for date in dates_list:
        if date is not None and date > max_date:
            max_date = date
        if date is not None and date < min_date:
            min_date = date

    chart_start_date = min_date - timedelta(days=10)
    chart_end_date = max_date + timedelta(days=55)
    chart_start_date = chart_start_date.date()
    chart_end_date = chart_end_date.date()
    category = []
    while chart_start_date <= chart_end_date:
        temp_category = {"start": chart_start_date.strftime('%d/%m/%Y')}
        endOfMonth = calendar.monthrange(chart_start_date.year, chart_start_date.month)[1]
        temp_category["end"] = datetime(year=chart_start_date.year, month=chart_start_date.month,
                                        day=endOfMonth).date().strftime('%d/%m/%Y')
        temp_category["label"] = str(chart_start_date.strftime('%B'))
        category.append(temp_category)
        if chart_start_date.month >= 12:
            chart_start_date = datetime(chart_start_date.year + 1, 1, 1).date()
        else:
            chart_start_date = datetime(chart_start_date.year, chart_start_date.month + 1, 1).date()

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
    task_field = {'DLT1a': '3', 'DLT1b1': '2', 'DLT1b2': '2', 'DLT1c': '2', 'DLT2': '10', 'DLT3a1': '4', 'DLT3a2': '55',
                  'DLT3b1': '10', 'DLT3b2': '25', 'DLT3b3': '5', 'DLT3b4': '5', 'DLT3d': '7', 'DLT3e': '5',
                  'DLT4a': '10', 'DLT4b': '1'
                  }

    def estimate_task(est_task):
        if dates_list[indx] is not None and values[indx] != -1:
            estimated_task = {'label': 'Estimated_' + str(est_task[0]) + ' -  ' + str(est_task[1]) + ' days',
                              'processid': str(int(indx + 1)), 'id': str(est_task[0]), 'color': TASK_ESTIMATED_COLOR,
                              'height': '15%',
                              'toppadding': '25%', 'start': date_format(dates_list[indx]),
                              'end': date_format(dates_list[indx] + timedelta(days=int(est_task[1])))}
            task.append(estimated_task)

    def actual_task(act_task):
        if dates_list[indx] is not None and values[indx] != -1:
            actual = {'label': 'Actual_' + str(act_task[0]) + ' -  ' + str(values[indx]) + ' days - ' +
                               str(count_per_step[indx]) + ' orders', 'processid': str(int(indx + 1)), 'height': '32%',
                      'toppadding': '56%', 'id': str(act_task[0]), 'color': TASK_ACTUAL_COLOR,
                      'start': date_format(dates_list[indx]),
                      'end': date_format(dates_list[indx] + timedelta(days=int(values[indx])))}
            task.append(actual)

    indx = 0
    task_field = sorted(task_field.items())
    for field in task_field:
        estimate_task(field)
        actual_task(field)
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
