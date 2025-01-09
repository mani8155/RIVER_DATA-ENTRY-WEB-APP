from django.contrib import messages
from django.shortcuts import render, redirect
import requests as req
import json, hashlib
from .models import *
from django.http import JsonResponse



# def user_bundle_settings():
#     obj = SettingsModel.objects.get(id=1)
#     return obj.api_url

def get_settings_ajax(request):

    obj = SettingsModel.objects.get(id=1)
    data = {
        'application_name': obj.application_name,
        'favicon_caption': obj.favicon_caption,
        'favicon_logo': obj.favicon_logo.url,
    }
    return JsonResponse(data)
  # else:
  #   return {}


def settings_screen(request):
    obj = SettingsModel.objects.all()

    context = {
        "menu": "menu-settings",
        "obj": obj,

    }
    return render(request, 'settings_views/settings_screen.html', context)


def settings_form(request, id):
    obj = SettingsModel.objects.get(id=id)
    # print(obj)

    if request.method == 'POST':
        app_name = request.POST['app_name']
        api_url = request.POST['api_url']
        favicon_caption = request.POST['favicon_caption']
        favicon_file = request.FILES.get('favicon_file')

        if favicon_file is None:
            obj.application_name = app_name
            obj.api_url = api_url
            obj.favicon_caption = favicon_caption
            obj.save()
            return redirect('settings_screen')

        else:
            obj.application_name = app_name
            obj.api_url = api_url
            obj.favicon_caption = favicon_caption
            obj.favicon_logo = favicon_file
            obj.save()

            return redirect('settings_screen')

    context = {
        "menu": "menu-settings",
        "obj": obj,
    }
    return render(request, 'settings_views/settings_form.html', context)

