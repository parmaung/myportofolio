from django.contrib import admin

from main.models import Education, Experience, Project, Skills

admin.site.register(Experience)
admin.site.register(Project)
admin.site.register(Education)
admin.site.register(Skills)
