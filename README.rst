Programmer's Documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

vcms.www
=========

WWW - CMS Menu
---------------


CMS Menu models is what makes pages appears on the site.

They are responsible for: 

- Linking page or other generic type(ex. links) to menu navigation 
- Make page hidden or to be displayed in menu
- Create url scheme

WWW - BasicPage
----------------

Master parent of the CMS page system. If you want to create a new page types, you should inherit from this models.

- Sets all basic parameters needed
- Make page available (publish) or unavailable (draft)
- Sets the type of it's container (absolute, relative)

The content of a page is made by adding widgets to it. To hold them the page should define containers.

WWW - ContainerWidgets
-----------------------

Make the links between widgets and a page. A widget can be anything (generic relation) as long as it provide a render method.

A container position the widget as specified in the BasicPage Model.


Overview
=========

Workflow
--------

.. list-table:: Basic CMS workflow
  :widths: 20 34 30
  :header-rows: 1

  * - Condition
    - Action
    - Effect
  * - Request
    - Middle called and validate if url in models CMSMEnu
    -
  * - If in CMSMenu
    - Fetch the menu's page and request controller associated to it
    - CMSMenu request_processor set default variable
  * - 
    - Page gets containers, Render all wingets for all containers
    - Return HTMl
  * - If not in CMSMenu
    - Execute normal django urlpatterns
    - 

Models hierachy
---------------


CMSMenu

======================== =====================================================================
Provide                   Generic Relation should implement
======================== =====================================================================
slug (url)
Geniric relation needed   get_controller : return a controller function to call if menu acces
======================== =====================================================================


BasicPage ( Can be inherited )

======================== ===============================================================
Provide                   Children should implement
======================== ===============================================================
Basic page information    containers tuple (container slug, container translatable name)

                          containers_type dict { container slug : [relative, absolute] }
======================== ===============================================================


ContainerWidgets

================================ =======================================================
Provide                          Requires
================================ =======================================================
Map widget to a page containers  From page : containers_type for layout

                                 From page : containers
================================ =======================================================

Widget ( Can be inherited )

================================ =================================================
Provide                          Should implement
================================ =================================================
html part that construct a page  get_absolute_url

                                 render method : return html
================================ =================================================



AUTHORS
~~~~~~~~
Francis Lavoie
