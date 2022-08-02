from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Source)
admin.site.register(Updates)
admin.site.register(Credentials)
admin.site.register(Source_Data)
admin.site.register(Metric)
admin.site.register(Metric_Data)
admin.site.register(Metric_Types)
admin.site.register(Artifact)

