from django.contrib import admin
import nested_admin
from .models import *


admin.site.site_header = 'Polskie organy piszczałkowe'
admin.site.site_title = 'Polskie organy piszczałkowe'


class StopInline(nested_admin.NestedTabularInline):
    model = Stop
    extra = 0


class KeyboardInline(nested_admin.NestedStackedInline):
    model = Keyboard
    extra = 0
    inlines = [StopInline]


class PhotoInline(nested_admin.NestedTabularInline):
    model = Photo
    extra = 0


class WorkInline(nested_admin.NestedStackedInline):
    model = Work
    extra = 0


@admin.register(Instrument)
class InstrumentAdmin(nested_admin.NestedModelAdmin):
    list_display = ['region_name', 'location', 'comment', 'stops', 'published']
    list_display_links = ['location', 'comment']
    list_filter = ['published', 'location__city__region']
    search_fields = ['location__name', 'location__city__name', 'location__city__region__name', 'comment']
    inlines = [PhotoInline, KeyboardInline, WorkInline]


@admin.register(Recording)
class RecordingAdmin(admin.ModelAdmin):
    list_display = ['description', 'performer', 'instrument']
    search_fields = ['description', 'performer__name', 'instrument__comment', 'instrument__location__name',
                     'instrument__location__city__name', 'instrument__location__city__region__name']


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    search_fields = ['name']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'region']
    list_filter = ['region']
    search_fields = ['name', 'region__name']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'city']
    list_filter = ['city__region']
    search_fields = ['name', 'city__name', 'city__region__name']


@admin.register(Builder)
class BuilderAdmin(admin.ModelAdmin):
    pass


class SampleInline(admin.TabularInline):
    model = Sample
    extra = 0


@admin.register(StopType)
class StopTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['families__name']
    search_fields = ['name', 'families__name']
    filter_horizontal = ['families']
    inlines = [SampleInline]


@admin.register(StopFamily)
class StopFamilyAdmin(admin.ModelAdmin):
    pass


@admin.register(Performer)
class PerformerAdmin(admin.ModelAdmin):
    pass


@admin.register(Concert)
class ConcertAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'instrument']
    list_filter = ['instrument__location__city__region']
    search_fields = ['name', 'date', 'instrument__comment', 'instrument__location__name',
                     'instrument__location__city__name', 'instrument__location__city__region__name']
    filter_horizontal = ['performers']
