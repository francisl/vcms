# -*- coding: UTF8 -*-
# Application : CMS
# Module : Products
# Copyright (c) 2011 Vimba inc. All rights reserved.
# Created by Francis Lavoie on Jan 22 2011.

import re

class HtmlReduce(object):
    def __init__(self, html, length=3):
        self.html = html
        self.length = length
        
    def get_html(self):
        reg = re.compile(r"<p(?:.*?)>(.*?)<\/p>")
        preview = ""
        compress_html = self.html.replace('\n', '')
        all_found = reg.findall(compress_html)
        preview_length = self.length if len(all_found) >= self.length else len(all_found)
        for found in all_found[:preview_length]:
            preview += '<p>' + found + '</p>'
        return preview