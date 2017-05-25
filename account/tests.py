import unittest

import os
import sys

from django.conf import settings

from django.core.wsgi import get_wsgi_application

sys.path.append("/home/alexander/projects/web/bank")

os.environ['DJANGO_SETTINGS_MODULE'] = 'bank.settings'
application = get_wsgi_application()

# settings.configure(TEMPLATE_DIRS=('./templates/',), DEBUG=False,
#                            TEMPLATE_DEBUG=False)

import account
import account.models
from account.models import User
import account.views

def init():
    account.models.User.objects.all().delete()
    u = User(inn = "1", name = "User1", money = 300)
    u.save()
    result = u.id
    u = User(inn = "2", name = "User2", money = 100)
    u.save()
    u = User(inn = "3", name = "User3", money = 100)
    u.save()
    return result

class TestStringMethods(unittest.TestCase):

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_ok(self):
        _id = init()
        flag = account.views.transmit({"sender": _id, "receivers": "2 3", "sum": "200"})
        result = ([ u.money for u in  User.objects.order_by("name").all()])
        self.assertEqual(result, [100.0, 200.0, 200.0])

    def test_sender_not_found(self):
        _id = init()
        with self.assertRaises(account.views.SenderNotFoundError):
            account.views.transmit({"sender": "-1", "receivers": "2", "sum": "200"})

    def test_receiver_not_found(self):
        _id = init()
        with self.assertRaises(account.views.ReceiverNotFoundError):
            account.views.transmit({"sender": _id, "receivers": "42", "sum": "200"})

    def test_sum_not_valid(self):
        _id = init()
        with self.assertRaises(account.views.SumNotValidError):
            account.views.transmit({"sender": _id, "receivers": "2", "sum": "ErrorValue"})

    def test_money_not_enough(self):
        _id = init()
        with self.assertRaises(account.views.MoneyNotEnoughError):
            account.views.transmit({"sender": _id, "receivers": "2", "sum": "200000"})


if __name__ == '__main__':
    unittest.main()
