# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie

def create_tree_structure(name, items=[], child_selected=False, selected=False, url="#"):
    """ Take required parameters and return a valid dictionary tree node 
    """
    return { "name": name, 
            "items": items, 
            "child_selected":child_selected, 
            "selected":selected, 
            "url":url }
