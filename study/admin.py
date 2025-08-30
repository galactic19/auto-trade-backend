from django.contrib import admin

from study.models import StudyModel


@admin.register(StudyModel)
class StudyAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    list_filter = ('created_at', 'updated_at')
