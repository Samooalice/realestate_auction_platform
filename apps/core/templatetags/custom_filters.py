from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    """값에 arg를 곱합니다."""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def divide(value, arg):
    """값을 arg로 나눕니다."""
    try:
        return int(value) / int(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0


@register.filter
def format_price(value):
    """가격을 억/만원 단위로 포맷합니다."""
    try:
        value = int(value)
        if value >= 100000000:
            return f'{value / 100000000:.1f}억'
        elif value >= 10000:
            return f'{value / 10000:.0f}만'
        return f'{value:,}'
    except (ValueError, TypeError):
        return value
