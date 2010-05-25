# encoding: utf-8
# copyright Vimba inc. 2010
# programmer : Francis Lavoie

from django import template
from django.template.loader import render_to_string

def create_button(name, url, type='text', input_type="submit"):
    """ return a button dictionary
        ˙
        @param name: name to display
        @param url: target
        @param type: type of button, valid option are 'text' or 'input'
        @param input: type: if type == input, option are 'reset' or 'submit'
        
        @example:
            >>> from vcms.apps.vwm import button.generator
            
            # create one item 
            >>> buttons_list = []
            >>> buttons_list.append(button.generator.create_button('Action1', 'http://www.test.com', 'text'))

    """
    
    return {'name':name,'url':url, 'type':type}
