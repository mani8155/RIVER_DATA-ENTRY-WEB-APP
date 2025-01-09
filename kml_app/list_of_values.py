import openpyxl
import requests as rq
from django.db import IntegrityError
from django.shortcuts import render, redirect
from .models import *
from .forms import ListOFValuesForm
from django.contrib import messages
import configparser
import os


from django.http import HttpResponse
from openpyxl import load_workbook

# from .usermanegement import fetch_user_credential

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'config.ini'))

ListOFValues_EXCEL_API_URL = config['DEFAULT']['ListOFValues_EXCEL_API_URL']

def get_all_values(request):
    # user_type = fetch_user_credential(request, username)
    obj = ListOFValues.objects.all().order_by('list_type__list_type', 'list_of_values')
    context = {"menu": "menu-list-values", "obj": obj, }
    return render(request, 'list_of_values/list_of_values.html', context)


def search_values(request):
    search_query = request.GET.get('search', '')
    search_filter = (
            Q(list_of_values__icontains=search_query) |
            Q(list_type__list_type__icontains=search_query)  # Use the correct field from ListType
    )

    obj = ListOFValues.objects.filter(search_filter).order_by('list_type__list_type')
    # print(obj)
    context = {"menu": "menu-list-values", "obj": obj, "search_query": search_query}
    return render(request, 'list_of_values/list_of_values.html', context)


def new_list_of_values_entry(request):
    form = ListOFValuesForm()
    if request.method == 'POST':
        form = ListOFValuesForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.list_of_values = obj.list_of_values
            obj.list_type = obj.list_type
            obj.active = obj.active
            obj.dupcheck = f"{obj.list_type}{obj.list_of_values}{obj.active}"
            try:
                obj.save()
                return redirect('list-of-values')
            except IntegrityError as e:
                messages.error(request, message="Data already exists.")
        else:
            messages.error(request, message="Form is not valid")

    context = {"menu": "menu-list-values", "form": form, "head": "New List of Values",
               }
    return render(request, 'list_of_values/list_values_form.html', context)


def edit_list_of_values(request, id):
    data = ListOFValues.objects.get(id=id)
    form = ListOFValuesForm(instance=data)

    if request.method == 'POST':
        form = ListOFValuesForm(request.POST, instance=data)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.list_of_values = obj.list_of_values
            obj.dupcheck = f"{obj.list_type}{obj.list_of_values}{obj.active}"
            try:
                obj.save()
                return redirect('list-of-values')
            except IntegrityError as e:
                messages.error(request, message="Data already exists.")
        else:
            messages.error(request, message="Form is not valid")

    context = {"menu": "menu-list-values", "form": form, "head": "Edit List of Values"}
    return render(request, 'list_of_values/list_values_form.html', context)


def delete_list_of_values(request, id):
    data = ListOFValues.objects.get(id=id)

    if request.method == 'POST':
        try:
            data.delete()
            return redirect('list-of-values')
        except models.ProtectedError as e:
            messages.error(request, message="You Can't Delete this Transaction Child Records are Available")
            return redirect('list-of-values')
        except IntegrityError as e:
            messages.error(request, message="IntegrityError: {e}")

    context = {"menu": "menu-list-values", "obj": data}
    return render(request, 'list_of_values/list_value_delete.html', context)


def list_of_values_excel(request):
    if request.method == 'POST':
        if 'upload_file' in request.FILES:
            upload_file = request.FILES['upload_file']
            # print(upload_file)
            upload_file_name = upload_file.name

            api_url = ListOFValues_EXCEL_API_URL

            # Prepare the payload and files for the POST request
            payload = {}
            files = [('excel_file', (upload_file_name, upload_file.read(),
                                     'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))]
            headers = {}

            # Send the POST request to the API endpoint
            response = rq.request("POST", api_url, headers=headers, data=payload, files=files)

            try:
                response_data = response.json()
                if 'Status' in response_data:

                    message = (
                        f"""{response_data['Status']}
                            No of Records In Excel: {response_data['total_rows']}
                            No of Records Imported: {response_data['create_obj_count']}
                            No of Records Updated: {response_data['existing_obj_count']}"""
                    )
                    messages.success(request, message)

                elif 'error' in response_data:
                    messages.error(request, message=response_data['error'])
                else:
                    messages.error(request, message="Unexpected response from the server")
            except ValueError:
                messages.error(request, message="Invalid JSON response from the server")

            return redirect('list-of-values')

    return HttpResponse("Invalid request method or file not provided")


def sample_excel_list_of_values(request):
    media_file_path = 'media/sample_excels/list_of_values.xlsx'

    with open(media_file_path, 'rb') as file:
        response = HttpResponse(file.read(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="list_of_values_sample.xlsx"'
        return response