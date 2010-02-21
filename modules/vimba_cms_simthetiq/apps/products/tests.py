# -*- coding: UTF8 -*-

# Vimba CMS - Products
# Application : CMS
# Module : Products
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by François Lebel on 10-02-20.

from django.test import TestCase
from django.core.files import File as DjangoFile
from models import *


class VideoTest(TestCase):
    def test_filesize_mimetype_flv(self):
        video_file = DjangoFile(open(os.path.dirname(os.path.realpath( __file__ )) + "/testdata/foosball.flv"), "foosball.flv")
        vid = Video.objects.create(name="Test FLV", file=video_file)
        vid.tags.create(tagname="Test tag")
        vid.save()
        video_filesize = video_file.size
        self.assertEquals(vid.file.size, video_filesize)
        video_file.close()
        self.assertEquals(vid.mime_type, "video/x-flv")
        vid.delete() # Make sure we don't leave the file on the filesystem

    def test_filesize_mimetype_mov(self):
        video_file = DjangoFile(open(os.path.dirname(os.path.realpath( __file__ )) + "/testdata/sample_iTunes.mov"), "sample_iTunes.mov")
        vid = Video.objects.create(name="Test MOV", file=video_file)
        vid.tags.create(tagname="Test tag")
        vid.save()
        video_filesize = video_file.size
        self.assertEquals(vid.file.size, video_filesize)
        video_file.close()
        self.assertEquals(vid.mime_type, "video/quicktime")
        vid.delete() # Make sure we don't leave the file on the filesystem

    def test_filesize_mimetype_swf(self):
        video_file = DjangoFile(open(os.path.dirname(os.path.realpath( __file__ )) + "/testdata/test-embeded.swf"), "test-embeded.swf")
        vid = Video.objects.create(name="Test SWF", file=video_file)
        vid.tags.create(tagname="Test tag")
        vid.save()
        video_filesize = video_file.size
        self.assertEquals(vid.file.size, video_filesize)
        video_file.close()
        self.assertEquals(vid.mime_type, "application/x-shockwave-flash")
        vid.delete() # Make sure we don't leave the file on the filesystem
