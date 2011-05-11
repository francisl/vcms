Programmer's Documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Building blocks
=================

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

Workflow
=========

::

Request --> Middleware check if requested url in menu --(no)--> Continu normal django url patterns --(no)--> Return 404
                            | (yes)                                          |(yes)
                            v                                                v
           Ask page to return controller and execute it                Return Html
                            |
                            v
                         For all Container
                         - For all Widger
                         -- Call Render
                            |
                            v
                        Return Html



AUTHORS
~~~~~~~~
Francis Lavoie
