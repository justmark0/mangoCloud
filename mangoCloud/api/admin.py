from django.contrib import admin
from .models import File

admin.site.register(File)


class MyModelAdmin(admin.ModelAdmin):
    class Media:
        css = {
             'all': ('../backend/static/admin_css.css',)
        }

