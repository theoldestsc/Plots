from django.contrib import admin
from .models import Plot
from django.utils.safestring import mark_safe
# Register your models here.


def image_tag(obj):
    return mark_safe('<img src="{}" width =300 height=120/>'.format(obj.image.url))
image_tag.short_description = 'Image'


@admin.register(Plot)
class PlotAdmin(admin.ModelAdmin):
    list_display = ['user', image_tag, 'function', 'date', 'interval','step',]
    readonly_fields = [image_tag]
