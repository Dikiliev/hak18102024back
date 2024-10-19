from django.contrib import admin
from .models import ApplicationType, Application, ApplicationComment, ApplicationField

admin.site.register(ApplicationType)
admin.site.register(Application)
admin.site.register(ApplicationComment)
admin.site.register(ApplicationField)

