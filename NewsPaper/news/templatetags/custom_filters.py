from django import template

register = template.Library()

bad_words = ["дурак", "дура", "дураки", "редиска", "редиски"]

@register.filter()
def censor(value):
    for i in bad_words:
        value = value.replace(i[1:], '*' * len(i[1:]))
    return value