from django import template


register = template.Library()

@register.filter(name="division")
def division(value, args):
    price = int(value)
    return price / args