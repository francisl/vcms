# encoding: utf-8
# copyright Vimba inc. 2010
# programmer : Francis Lavoie

from django import template
from django.template.loader import render_to_string

def create_button(name, url, type='text'):
    """ return a button dictionary
        ˙
        @param name: name to display
        @param url: target
        @param type: type of button, valid option are 'test', 'input_reset', 'input_submit'
        
        @example:
            >>> from vcms.apps.vwm import button.generator
            
            # create one item 
            >>> buttons_list = []
            >>> buttons_list.append(button.generator.create_button('Action1', 'http://www.test.com', 'text'))

    """
    
    return {'name':name,'url':url, 'type':type}

def generate_buttons(buttons, css_id="", css_class=""):
    """ generate and html button list
    
        @param buttons: list of button dictionnary
        @param css_id: string id of the list container
        @param css_class: string, class name of thelist container
        
        @example:
            >>> from vcms.apps.vwm import button.generator
            
            # create one item 
            >>> buttons_list = []
            >>> buttons_list.append(button.generator.create_button('Action1', 'http://www.test.com', 'text'))
            >>> buttons_list.append(button.generator.create_button('Action2', 'http://www.test2.com', 'text'))
            >>> button_html = button.generator.generate_buttons(buttons_list)

    """
    return {"buttons":buttons, "cssid":cssid, "cssclass": cssclass}
