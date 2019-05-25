from rest_framework.views import APIView, status, Response
from .services import *
from django.http import Http404
from rest_framework import permissions
from common.models import *
from rest_framework.decorators import api_view
from common.serializers import *
from .construct_order_chart import *


class Search(APIView):
    def post(self, request):
        # check if nothing param to send or wrong param sent
        if len(request.body) == 0 or check_field_data(request.data):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        fields = build_model_query(request.data)  # retrieve the param data sent to json data

        order_detail = get_order_details(fields)  # Getting Order Details and DLts
        if len(order_detail) == 0:
            return Response(status=status.HTTP_204_NO_CONTENT)

        full_data = {'order_detail': order_detail}

        if full_data['order_detail'] == 0:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(full_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_order_xml(request):
    if len(request.body) == 0:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    order_chart = generate_order_json(request.data)

    if order_chart == 0:
        return Response(status=status.HTTP_204_NO_CONTENT)

    else:
        return Response(order_chart, status=status.HTTP_200_OK)


@api_view(['Post'])
def get_order_autocomplete(request):
    if len(request.body) == 0:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    searchfilter = {str(request.data) + "__isnull": False, 'num_fields__gt': 23}
    searchexclude = {str(request.data) + '__contains': 'NOTCOUNTED'}
    order_fields = DltOrderDetail.objects.filter(**searchfilter).exclude(**searchexclude).values(
        request.data).distinct().order_by(request.data)

    if order_fields == 0:
        return Response(status=status.HTTP_204_NO_CONTENT)

    else:
        return Response(order_fields, status=status.HTTP_200_OK)
