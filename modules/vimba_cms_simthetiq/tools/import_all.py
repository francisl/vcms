#!/usr/bin/env python
# -*- coding: utf-8 -*-

from vimba_cms_simthetiq.tools import images_import as ii
from vimba_cms_simthetiq.tools import product_import as pi



pi.importProducts(drop=True, debug=True)

ii.importImages(drop=True, debug=True)

pi.setOriginalImage(debug=True)

