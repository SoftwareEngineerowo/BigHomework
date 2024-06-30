import uuid

from django.test import TestCase

from aibot.views import getNum


class AibotTestCase(TestCase):
    def test_getNum(self):
        print(getNum('57C8F5F7-36A9-769C-26D3-6ED7C76D3602'))
