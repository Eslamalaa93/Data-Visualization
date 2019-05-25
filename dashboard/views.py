from rest_framework.views import APIView, status, Response
from .services import *
from django.http import Http404
from rest_framework import permissions
from common.models import *
from rest_framework.decorators import api_view
from common.serializers import *


@api_view(['POST'])
def get_dlt_target(request):
    if len(request.body) == 0:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    dlt_met_target = dlt_target()

    if len(dlt_met_target) == 0:
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(dlt_met_target, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_top_customer(request):
    if len(request.body) == 0:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    customers_top = top_customer()

    if len(customers_top) == 0:
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(customers_top, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_top_country(request):
    if len(request.body) == 0:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    country_top = top_country()

    if len(country_top) == 0:
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(country_top, status=status.HTTP_200_OK)
