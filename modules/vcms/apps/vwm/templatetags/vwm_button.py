# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie
from django import template

register = template.Library()

@register.inclusion_tag('button/button.html')
def generate_buttons(buttons, css_id="", css_class=""):
    """ generate and html button list
    
        @param buttons: list of button dictionnary
        @param css_id: string id of the list container
        @param css_class: string, class name of thelist container
        
        @example:
            >>> from vcms.apps.vwm import button.generator, templatetags
            
            # create one item 
            >>> buttons_list = []
            >>> buttons_list.append(button.generator.create_button('Action1', 'http://www.test.com', 'text'))
            >>> buttons_list.append(button.generator.create_button('Action2', 'http://www.test2.com', 'text'))

            then pass the buttons_list to your template
            in the template 
            {% load vwm_button %}
            {% generate_buttons buttons_list %}
         

    """
    return { "buttons":buttons, "css_id":css_id, "css_class": css_class }