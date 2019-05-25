from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^Dlt_Analysis/$', views.get_dlt_analysis)
]

urlpatterns = format_suffix_patterns(urlpatterns)
