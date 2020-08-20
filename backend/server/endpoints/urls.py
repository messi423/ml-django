from .views import *
from rest_framework import routers
from django.conf.urls import url, include


r = routers.DefaultRouter()
r.register('endpoints', EndpointView, basename='endpoints')
r.register('mlalgorithms', MLAlgorithmView, basename='mlalgorithms')
r.register('mlalgorithmstatus', MLAlgorithmStatusView, basename='mlalgorithmstatus')
r.register('mlrequests', MLRequestView, basename='mlrequests')
r.register('abtest', ABTestView, basename='abtest')

urlpatterns = [
    url(r"^api/v1/", include(r.urls)),
    url(r"^api/v1/(?P<endpoint_name>.+)/predict$", PredictView.as_view(), name="predict"),
    url(r"^api/v1/stop_ab_test/(?P<ab_test_id>.+)", StopABTestView.as_view(), name="stop_ab"),
]
