from django import template
import json
register = template.Library()

@register.filter
def get_chart_color(index):
    colors = [
        '#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b',
        '#858796', '#5a5c69', '#3a3b45', '#2e59d9', '#17a673'
    ]
    return colors[index % len(colors)]


@register.filter
def map_attr(items, attr):
    return [getattr(item, attr) for item in items]

# O para diccionarios:
@register.filter
def map_key(items, key):
    return [item[key] for item in items]


@register.filter
def to_json(value):
    return json.dumps(value)

@register.filter
def extract_values(items, key):
    return [item[key] for item in items]