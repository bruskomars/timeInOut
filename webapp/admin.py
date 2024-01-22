from django.contrib import admin
from .models import User, TimeInOut, GeneratedReport

# Register your models here.
admin.site.register(TimeInOut)
admin.site.register(GeneratedReport)
admin.site.register(User)