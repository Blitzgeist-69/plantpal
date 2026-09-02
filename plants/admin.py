from django.contrib import admin
from .models import Plant, CareLog

# Register your models here.


class CareLogInline(admin.TabularInline):
    model = CareLog
    extra = 0


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = (
        'nickname', 'species', 'user', 'location', 'water_frequency_days',
    )
    list_filter = ('light_needs',)
    search_fields = ('nickname', 'species',)
    inlines = [CareLogInline]


@admin.register(CareLog)
class CareLogAdmin(admin.ModelAdmin):
    list_display = ('plant', 'action', 'date',)
    list_filter = ('action',)
    date_hierarchy = 'date'
