from django import template

register = template.Library()

@register.inclusion_tag('avatar_menu.html', takes_context=True)
def avatar_menu(context):
    user = context['user']
    return {'user': user}