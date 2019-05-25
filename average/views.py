from rest_framework.views import APIView, status, Response
from common.serializers import *
from .services import *
from django.http import Http404
from rest_framework import permissions
from rest_framework.decorators import api_view


@api_view(['Post'])
def get_dlt_orders_average(request):
    if len(request.body) == 0:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    charts = request.data

    average_service = AverageService()
    fields_param = {'cutdate__range': [charts['start_date'], charts['end_date']]}
    result = average_service.get_dlt_orders_steps_average_chart(fields_param)

    if len(result['chart_json']['tasks']) == 0:
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(result, status=status.HTTP_200_OK)


@api_view(['Post'])
def performance_dlt_average(request):
    if len(request.body) == 0:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    charts = request.data

    average_service = AverageService()

    fields_param = {'cutdate__range': [charts['firstChart']['start_date'], charts['firstChart']['end_date']]}
    first_chart_result = average_service.get_dlt_orders_steps_average_chart(fields_param)

    fields_param = {'cutdate__range': [charts['secondChart']['start_date'], charts['secondChart']['end_date']]}
    second_chart_result = average_service.get_dlt_orders_steps_average_chart(fields_param)

    if len(first_chart_result['chart_json']['tasks']) == 0 or len(second_chart_result['chart_json']['tasks']) == 0:
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        charts_result = {'first_chart': first_chart_result, 'second_chart': second_chart_result}
        return Response(charts_result, status=status.HTTP_200_OK)


@api_view(['Post'])
def dlt_analysis_visualization(request):
    if len(request.body) == 0:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    average_service = AverageService()
    first_chart_result = average_service.get_dlt_orders_steps_average_chart(request.data)

    if len(first_chart_result['chart_json']['tasks']) == 0:
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(first_chart_result, status=status.HTTP_200_OK)
