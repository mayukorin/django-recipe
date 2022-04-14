from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def ingredient_img_path(value):
    return "images/" + value + ".jpg"

@register.filter
@stringfilter
def ingredient_img_path2(value):
    return "images/trial/" + value + ".jpg"



@register.filter
@stringfilter
def ingredient_mini_img_path(value):
    return "images/" + value + "-mini.jpg"