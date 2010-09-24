# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie
from django import template
from vcms.www.models.containers import PageContainer, ContainerWidgets

register = template.Library()

@register.inclusion_tag('containers/relative.html')
def relative_container(current_page, container_name):
    page_container = PageContainer.objects.get_container_for_page_of_type(current_page, 'relative', container_name)
    widgets = ContainerWidgets.objects.get_widgets_for_container(page_container)
    return { 'widgets': widgets }

