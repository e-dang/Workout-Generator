from django.contrib import admin
from .models import Equipment


class EquipmentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Equipment, EquipmentAdmin)
