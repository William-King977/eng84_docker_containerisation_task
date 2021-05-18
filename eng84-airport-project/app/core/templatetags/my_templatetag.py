from django import template

register = template.Library()

@register.simple_tag
def at_index(data, index):
    return  data[index]
