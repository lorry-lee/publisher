"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from publisher.apps.post import scan_picture_url, html_to_text
from publisher.apps.post.views import submit_reply
from publisher.apps.post.models import *

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)

    def test_scan_picture(self):
        result = scan_picture_url("""<p><img alt="" width="180" height="136" src="/photologue/photos/fengxiao/2012.08.12/M_303.jpg" /></p>""")
        self.assertEqual(result, "/photologue/photos/fengxiao/2012.08.12/M_303.jpg")

    def test_html_to_text(self):
        result = html_to_text("<p>test&fjie;</p>")
        self.assertEqual(result, "test")

    def test_submit_reply(self):
        class temp_obj(object):
            def __init__(self, d):
                setattr(self, 'POST', d)
                setattr(self, 'user', None)

        post = Post(title="title_test", type=0, content="content_test", is_public=True)
        post.save()
        request = temp_obj(dict())
        request.POST['post_id'] = post.pk
        request.POST['content'] = 'reply_test'
        self.assertEqual(submit_reply(request)['result'], 200)
        reply1 = Reply.objects.get(content='reply_test')
        request = temp_obj(dict())
        request.POST['post_id'] = post.pk
        request.POST['content'] = 'reply_test2'
        request.POST['parent'] = reply1.pk
        self.assertEqual(submit_reply(request)['result'], 200)
        reply2 = Reply.objects.get(content='reply_test2')
