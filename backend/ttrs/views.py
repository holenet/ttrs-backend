from django.http import HttpResponse
from django.shortcuts import render


def test(request):
    return HttpResponse("It's test page of ttrs app")
