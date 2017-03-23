from django.shortcuts import HttpResponse


def home_page(request):
    return HttpResponse("<html><title>To-Do lists</title></html>")
