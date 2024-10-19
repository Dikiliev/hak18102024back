from django.contrib import admin
from .models import ApplicationType, Application, ApplicationComment

admin.site.register(ApplicationType)
admin.site.register(Application)
admin.site.register(ApplicationComment)

