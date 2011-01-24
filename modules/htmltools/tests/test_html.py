# -*- coding: UTF8 -*-
# Application : CMS
# Module : Products
# Copyright (c) 2011 Vimba inc. All rights reserved.
# Created by Francis Lavoie on Jan 22 2011.

from django.test import TestCase
#from django.core.files import File as DjangoFile
#from mockito import *

from htmltools.html import HtmlReduce

class HtmlTest(TestCase):
    def setUp(self):
        self.html = """<p>
<object id="ESPN_VIDEO" width="384" height="216" allownetworking="all" allowscriptaccess="always" data="http://espn.go.com/videohub/player/embed.swf" type="application/x-shockwave-flash">
<param name="movie" value="http://espn.go.com/videohub/player/embed.swf" />
<param name="allowFullScreen" value="true" />
<param name="wmode" value="opaque" />
<param name="allowScriptAccess" value="always" />
<param name="allowNetworking" value="all" />
<param name="flashVars" value="id=6009138" />
</object>
</p>
<p>second</p>
<p>Third</p>
<p>&Fourth</p>
"""

    def test_html_reduce_should_return_the_exact_amount_of_paragrpah_requested(self):
        html_reduce_expected = """<p>
<object id="ESPN_VIDEO" width="384" height="216" allownetworking="all" allowscriptaccess="always" data="http://espn.go.com/videohub/player/embed.swf" type="application/x-shockwave-flash">
<param name="movie" value="http://espn.go.com/videohub/player/embed.swf" />
<param name="allowFullScreen" value="true" />
<param name="wmode" value="opaque" />
<param name="allowScriptAccess" value="always" />
<param name="allowNetworking" value="all" />
<param name="flashVars" value="id=6009138" />
</object>
</p>
<p>second</p>
<p>Third</p>"""
        html_reducer = HtmlReduce(self.html, 3)
        self.assertEqual(html_reducer.get_html(), html_reduce_expected.replace('\n', ''))
        
    def test_html_reduce_should_return_the_maximum_length_available_when_the_request_length_is_bigger(self):
        html_reduce_expected = """<p>
<object id="ESPN_VIDEO" width="384" height="216" allownetworking="all" allowscriptaccess="always" data="http://espn.go.com/videohub/player/embed.swf" type="application/x-shockwave-flash">
<param name="movie" value="http://espn.go.com/videohub/player/embed.swf" />
<param name="allowFullScreen" value="true" />
<param name="wmode" value="opaque" />
<param name="allowScriptAccess" value="always" />
<param name="allowNetworking" value="all" />
<param name="flashVars" value="id=6009138" />
</object>
</p>
<p>second</p>
<p>Third</p>
<p>&Fourth</p>
"""
        html_reducer = HtmlReduce(self.html, 5)
        self.assertEqual(html_reducer.get_html(), html_reduce_expected.replace('\n', ''))
        