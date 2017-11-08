from django.contrib import admin
from app.models import User, App


class AppAdmin(admin.ModelAdmin):
    list_display = ('app_name', 'version', 'size', 'release_time')


admin.site.register(App, AppAdmin)
admin.site.register(User)
# Register your models here.
