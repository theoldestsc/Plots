from django import template
from ..models import Plot

register = template.Library()

@register.simple_tag
def plotInfo(image):
    new_str = image.function + "\nStep: " \
              + image.step + " \nInterval:" \
              + image.interval + "\n" \
              + "Date: " + str(image.date)[:19]
    return new_str
