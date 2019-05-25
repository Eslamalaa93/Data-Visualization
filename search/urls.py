from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^search/$',views.Search.as_view()),
    url(r'^orderxml/$', views.get_order_xml),
    url(r'^orderautocomplete/$', views.get_order_autocomplete)
]

urlpatterns = format_suffix_patterns(urlpatterns)
