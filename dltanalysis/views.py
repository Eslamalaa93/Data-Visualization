from rest_framework.views import APIView, status, Response
from .services import *
from django.http import Http404
from rest_framework import permissions
from common.models import *
from rest_framework.decorators import api_view
from common.serializers import *


@api_view(['POST'])
def get_dlt_analysis(request):
    if len(request.body) == 0:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    dlt_anal = dlt_analysis_service(request.data)

    if len(dlt_anal) == 0:
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(dlt_anal, status=status.HTTP_200_OK)
