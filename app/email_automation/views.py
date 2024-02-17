from django.shortcuts import render
from django.http import JsonResponse

from .service import AutomationService


def index(request):
    AutomationService.trigger_fn()
    return JsonResponse({"message": "Hello, World!"})
