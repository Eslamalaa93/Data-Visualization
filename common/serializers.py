from rest_framework import serializers
from .models import *


class DltOrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DltOrderDetail
        fields = ('id', 'gold_ref', 'country', 'customername', 'customercode', 'cmp_productname', 'ldm',
                  'ldm_team', 'ldm_region', 'sdm', 'sdm_team', 'sdm_msc', 'ltc', 'pocm', 'pocm_team', 'pocm_msc',
                  'status')


class DltOrderDaysSerializer(serializers.ModelSerializer):
    id = DltOrderDetailSerializer(read_only=True)

    class Meta:
        model = DltOrderDays
        exclude = ('cutdate',)
