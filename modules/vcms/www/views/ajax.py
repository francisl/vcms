# encoding: utf-8
# copyright Vimba inc. 2010
# programmer : Francis Lavoie

from django.utils import simplejson
from django.core import serializers
from django.contrib.auth.decorators import login_required
#from django.http import HttpResponseRedirect
from django.http import HttpResponse

from vcms.www.models.page import BasicPage
from vcms.www.models.menu import MainMenu as mm

@login_required
def get_page_list(request):
    """ return a json dictionnay of all available page
        @return: ordered dictionnary
            menu_id : { id : int
                        ,menu_name : string
                        ,lft : int (element on the left)
                        ,rgt : int (element on the right)
                        ,slug : string
                        ,description : string
                        ,containers : { 
                            container_id : { name : string
                                            , type : string
                                            }
                                    }
                        ,pages: { (recursive) }
                        ,display_in_menu : boolean
                        ,published: int (0 = draft, 1=published)
                    }
    """
    
    if request.method == 'GET':
        pages = BasicPage.objects.get_all_basic()
        mainmemu = mm.objects.get(menu_name='english')
        print("all basic page = %s" % pages)
        pages_dict = {"name":'english'
                      ,"pages": []
                      }

        for page in mainmemu.get_children():
            pages_dict['pages'].append({ "name": page.menu_name
                                    ,"id" : page.content_object.id
                                    ,"left" : page.lft
                                    ,"right" : page.rgt
                                    ,"menu_name" : page.menu_name
                                    ,"slug" : page.content_object.slug
                                    ,"description": page.content_object.description
                                    ,"containers" : {}
                                    ,"pages" : []
                                    ,"displayed" : page.display
                                    ,"published" : page.content_object.status
                                    })
        print("dict to json : %s " % pages_dict)
        return HttpResponse(simplejson.dumps(pages_dict), mimetype='application/javascript')
        

@login_required
def add_new_page(request):
    pass

@login_required
def update_page(request):
    pass

