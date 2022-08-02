from .views import *
from django.urls import path

urlpatterns = [
    path('sources/<slug>/<secret>', sources.as_view(), name='sources'),
    path('updater/', UpdaterView.as_view(), name='updater.sh'),
    path('metrics_creator/', MetricsCreatorView.as_view(), name='metrics'),
    path('collector/', CollectorView.as_view(), name='collections'),
    path('metrics/all/', MetricsDataView.as_view(), name='collections'),
    path('vpn/', VPNStatusCheck.as_view(), name='vpn'),
]