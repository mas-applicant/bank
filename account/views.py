#!/usr/bin/python
# -*- coding: utf8 -*-

from django.db import transaction

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

from django.template import loader
from django.template import Context

from django.shortcuts import render_to_response
from django import forms
from django.http import HttpResponseRedirect
from django.template import Template, RequestContext

from account.models import User

class AccountError(Exception):
    pass

class SenderNotFoundError(AccountError):
    pass

class ReceiversNotDefinedError(AccountError):
    pass

class ReceiverNotFoundError(AccountError):
    pass

class SumNotValidError(AccountError):
    pass

class MoneyNotEnoughError(AccountError):
    pass

class TransactionError(AccountError):
    pass

def main(request):
    t = loader.get_template('index.html')
    c = {'foo': 'bar'}
    c["users"] = []
    for user in User.objects.all():
        c["users"].append((user.id, user.name))
    return render(request, 'index.html', c)

def transmit(data):
    senders = list(User.objects.filter(id = int(data["sender"])).all())
    if len(senders) == 0:
        raise SenderNotFoundError(1, "Отправитель не найден")
    if data["receivers"] == "":
        raise ReceiversNotDefinedError(2, "Получатели не указаны")
    sender = senders[0]
    receivers = []
    for receiver in data["receivers"].split(" "):
        subreceivers = list(User.objects.filter(inn = receiver).all())
        if len(subreceivers) == 0:
            raise ReceiverNotFoundError(3, "Получатель с ИНН {} не найден".format(receiver))
        else:
            receivers.extend(subreceivers)
    try:
        _sum = float(data["sum"])
    except:
        raise SumNotValidError(4, "Введенная сумма {} не является корректной".format(data["sum"]))
    if _sum > sender.money:
        raise MoneyNotEnoughError(5, "На счету недостаточно средств")
    part = round(_sum / (1.0 * len(receivers)), 2)
    try:
        with transaction.atomic():
            sender.money = sender.money - _sum
            sender.save()
            for receiver in receivers:
                receiver.money = receiver.money + part
                receiver.save()
    except Exception as e:
        raise TransactionError(6, "Транзакция прошла неуспешно с ошибкой {}".format(e.args[0]))
    money = ([ u.money for u in  User.objects.order_by("name").all()])
    return True

def transmitRest(request):
    result = {"message": "Отправление средств прошло успешно", "code": 0}
    data = {}
    data["sender"] = request.POST["sender"]
    data["receivers"] = request.POST["receivers"]
    data["sum"] = request.POST["sum"]
    print('DATA', data)
    try:
        transmit(data)
    except AccountError as e:
        result["code"] = e.args[0]
        result["message"] = e.args[1]
    except Exception as e:
        result["code"] = -1
        result["message"] = e.args[0]
    return JsonResponse(result)
