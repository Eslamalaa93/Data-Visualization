from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^average/', views.get_dlt_orders_average),
    url(r'^performanceDlt/', views.performance_dlt_average),
    url(r'^dlt_analysis_visualization/', views.dlt_analysis_visualization)
]

urlpatterns = format_suffix_patterns(urlpatterns)
