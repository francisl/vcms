# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie
from django import template
from vcms.www.models.containers import ContainerWidgets

register = template.Library()

@register.inclusion_tag('containers/relative.html')
def relative_container(current_page, container_name):
    widgets = ContainerWidgets.objects.get_published_widget(current_page, container_name)
    return { 'widgets': widgets, 'container_name':container_name }

@register.inclusion_tag('containers/absolute.html')
def absolute_container(current_page, container_name):
    widgets = ContainerWidgets.objects.get_published_widget(current_page, container_name)
    return { 'widgets': widgets, 'container_name':container_name }
    