from . import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

admin.site.register(models.Member, UserAdmin)
admin.site.register(models.NAGroup)
admin.site.register(models.Codes)
admin.site.register(models.MeetingTime)
admin.site.register(models.Address)
admin.site.register(models.Meeting)
