from django.contrib import admin
from muscles.models import *


class MuscleSubPortionAdmin(admin.ModelAdmin):
    list_display = ('name', 'other_names')


class MuscleAdmin(admin.ModelAdmin):
    list_display = ('name', 'other_names', 'get_subportions')

    def get_subportions(self, obj):
        return '\n'.join([subportion.name for subportion in obj.subportions.all()])

    get_subportions.short_description = 'SubPortions'


class MuscleGroupingAdmin(admin.ModelAdmin):
    list_display = ('name', 'other_names', 'get_muscles')

    def get_muscles(self, obj):
        return '\n'.join([muscle.name for muscle in obj.muscles.all()])

    get_muscles.short_description = 'Muscles'


admin.site.register(MuscleSubPortion, MuscleSubPortionAdmin)
admin.site.register(Muscle, MuscleAdmin)
admin.site.register(MuscleGrouping, MuscleGroupingAdmin)
