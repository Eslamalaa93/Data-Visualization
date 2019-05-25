from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^Dlt_Target/', views.get_dlt_target),
    url(r'^Top_Customer/', views.get_top_customer),
    url(r'^Top_Country/', views.get_top_country)
]

urlpatterns = format_suffix_patterns(urlpatterns)
