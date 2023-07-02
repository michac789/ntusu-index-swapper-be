from django.contrib import admin
from indexswapper.models import CourseIndex, SwapRequest


class SwapRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'current_index',
        'status', 'wanted_indexes')


admin.site.register(CourseIndex)
admin.site.register(SwapRequest, SwapRequestAdmin)
