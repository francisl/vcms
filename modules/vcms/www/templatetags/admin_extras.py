from django import template
from django.template import Node
from vcms.www.models.page import BasicPage as Page

register = template.Library()

@register.inclusion_tag('admin/www/page/page_table.html')
def show_menu_table(lang='en'):
    menu_list = Page.objects.get_RootMenu()
    submenu_list = Page.objects.filter(level=1)

    submenus = {}
    for menu in menu_list:
        submenu  = Page.objects.get_SubMenu(menu)[0]
        submenus[menu.id] = {"menu": menu.id, "submenu": submenu }

    all_pages = Page.objects.get_Published()

    modules = Page.objects.values('module').order_by("module").distinct()
    
    #Generate and dictionnary of page per modules
    # takes all published page on the web site
    # and separate it into modules
    """
    pages ={}
    for page in Page.objects.get_NotDisplay():
        if pages.has_key(page.module):
            pages[page.module].append(page)
        else:
           pages[page.module] = [page ]
    """
    
    return locals()


class get_editable_container_fields_node(Node):
    def __init__(self, type, args, kwargs, asvar):
        self.type = type
        self.args = args
        self.kwargs = kwargs
        self.asvar = asvar

    def render(self, context):
        from django.core.urlresolvers import reverse, NoReverseMatch
        args = [arg.resolve(context) for arg in self.args]
        kwargs = dict([(smart_str(k,'ascii'), v.resolve(context))
                       for k, v in self.kwargs.items()])
        # Hide the field if it is not editable, is auto created or is one of the fields inherited from BasicPage
        from vcms.www.models.page import BasicPage
        basicpage_fields = [field.attname for field in BasicPage._meta.fields]
        fields = [field for field in context[self.type]._meta.fields if field.editable and not field.auto_created and field.attname != "page_id" and field.attname not in basicpage_fields]
        if self.asvar:
            context[self.asvar] = fields
            return ''
        else:
            return fields


def get_editable_container_fields(parser, token):
    """ Returns the list of fields contained in the specified class. """
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least one argument"
                                  " (path to a view)" % bits[0])
    type = bits[1]
    args = []
    kwargs = {}
    asvar = None
    bits = bits[2:]
    if len(bits) >= 2 and bits[-2] == 'as':
        asvar = bits[-1]
        bits = bits[:-2]
    # Now all the bits are parsed into new format,
    # process them as template vars
    if len(bits):
        for bit in bits:
            match = kwarg_re.match(bit)
            if not match:
                raise TemplateSyntaxError("Malformed arguments to get_editable_container_fields tag")
            name, value = match.groups()
            if name:
                kwargs[name] = parser.compile_filter(value)
            else:
                args.append(parser.compile_filter(value))
    return get_editable_container_fields_node(type, args, kwargs, asvar)
get_editable_container_fields = register.tag(get_editable_container_fields)

@register.inclusion_tag('admin/tiny_mce_addons_with_javascript_requirements.html')
def add_tiny_mce_with_requirements_javascript():
    from django.core.context_processors import media
    return media('MEDIA_URL')
