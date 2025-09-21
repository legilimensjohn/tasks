from django.contrib import admin
from .models import Task

# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'status', 'created_at', 'due_date']
    list_filter = ['priority', 'status', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['-created_at']
