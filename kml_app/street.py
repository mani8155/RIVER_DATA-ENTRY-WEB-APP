import json
import requests as rq
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Q, ProtectedError
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from .models import *
from .forms import StreetForm, SurveyMasterForm
from django.contrib import messages
import configparser
import os

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'config.ini'))

STREET_EXCEL_API_URL = config['DEFAULT']['STREET_EXCEL_API_URL']

def new_street_entry(request):
    form = StreetForm()

    context = {"menu": "menu-street", "form": form}
    return render(request, 'street/street_form.html', context)


def street_form_json(request):
    # print("street function")
    if request.method == 'POST':
        data = json.loads(request.POST.get('output'))
        deviations = data.pop('deviations')
        # print(data)
        # print(deviations)
        cad_line = StreetForm(data)
        cad_line.save()

        obj = StreetMaster.objects.last()
        # print("obj", obj.id)
        for dev in deviations:
            # print("loop working")

            dev_obj = SurveyMaster(**dev, street_master_id=obj.id)
            dev_obj.save()

        return JsonResponse({'status': 'success'})

    else:

        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def get_block_details(request):
    block_name = request.GET.get('block_name', None)
    if block_name:
        block = BlockMaster.objects.get(id=block_name)
        # print(block)

        data = {
            'ward_name': block.ward_name,
            'town_name': block.town_name.town_name,
            'revenue_division_no': block.revenue_division_no,
            'taluk_name': str(block.taluk_name),
            'district_name': str(block.district_name),
        }
        # print(data)
        return JsonResponse(data)
    else:
        return JsonResponse({})


def edit_street_entry(request, id):
    data = StreetMaster.objects.get(id=id)
    form = StreetForm(instance=data)
    survey_master = SurveyMaster.objects.filter(street_master=data)

    survey_master_list = []

    for obj in survey_master:
        # Append the relevant data to the list
        survey_master_list.append({
            'street_name': obj.street_name,
            'survey_no': obj.survey_no,
            'classification': obj.classification,
            'sub_classification': obj.sub_classification,
            'langitutte': obj.langitutte,
            'lattitude': obj.lattitude

        })

    # print(survey_master_list)

    context = {"menu": "menu-street", "form": form, "survey_master_list": survey_master_list, "id": id}
    return render(request, 'street/edit_street_form.html', context)


def edit_street_form_json(request):
    # print("edit street function")
    if request.method == 'POST':
        data = json.loads(request.POST.get('output'))
        id = json.loads(request.POST.get('id'))
        # print(id)
        deviations = data.pop('deviations')
        # print(data)
        # print(deviations)

        previous_data = StreetMaster.objects.get(id=id)
        # print(previous_data)
        previous_data.delete()

        cad_line = StreetForm(data)
        cad_line.save()

        obj = StreetMaster.objects.last()
        # print("obj", obj.id)
        for dev in deviations:
            # print("loop working")

            dev_obj = SurveyMaster(**dev, street_master_id=obj.id)
            dev_obj.save()

        return JsonResponse({'status': 'success'})

    else:

        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


# ---------------------------------------------------------------------------------------------
def delete_street_entry(request, id):
    data = StreetMaster.objects.get(id=id)
    # print(data.block_name)

    if request.method == 'POST':
        # try:
        #     check = CadastralMaster.objects.filter(block=data.block_name) or CadastralEntry.objects.filter(block=data.block_name)
        #     if check:
        #        messages.error(request, message="You Can't Delete this Transaction Child Records  are Available")
        #     else:
        #         # print("jsdhfjsd")
        data.delete()
        # except ProtectedError as e:
        #     messages.error(request, message="You Can't Delete this Transaction Child Records  are Available")
        return redirect('list-of-street')

    context = {"menu": "menu-street", "obj": data}
    return render(request, 'street/street_delete.html', context)


def get_all_street_data(request):
    obj = StreetMaster.objects.all().order_by(
        'river_name__list_of_values',
        'sub_basin',
        'district_name',
        'taluk_name',
        'town_name',
        'block_name',
    )
    context = {"menu": "menu-street", "obj": obj}
    return render(request, 'street/street_list.html', context)


def street_form(request):
    form = StreetForm()

    if request.method == 'POST':
        form = StreetForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            dupcheck_value = f"{obj.river_name}{obj.block_name}{obj.sub_basin}{obj.district_name}{obj.town_name}{obj.taluk_name}"
            obj.dupcheck = dupcheck_value
            try:
                obj.save()
                obj = StreetMaster.objects.last()
                street_id = obj.id
                return redirect('child_stree_form', street_id)
            except IntegrityError as e:
                messages.error(request, message="Data already exists.")

    context = {"form": form, "menu": "menu-street"}
    return render(request, 'street/new_street_form.html', context)


def child_stree_form(request, id):
    parent = StreetMaster.objects.get(id=id)
    # id = parent.id
    # print(parent)
    form = SurveyMasterForm()
    obj = SurveyMaster.objects.filter(street_master=id)

    if request.method == 'POST':
        form = SurveyMasterForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            obj = form.save(commit=False)
            obj.dupcheck = f"{obj.lattitude}{obj.langitutte}"
            obj.street_master = parent

            try:
                obj.save()
                return redirect('child_stree_form', id)
            except IntegrityError as e:
                messages.error(request, message="Data already exists.")
                return redirect('child_stree_form', id)

        else:
            messages.error(request, message=form.errors)

    context = {"menu": "menu-street", "form": form, "parent": parent, "obj": obj}
    return render(request, 'street/child_street_form.html', context)


def child_street_edit(request, id, parent_id):
    # print(parent_id)
    # print(id)
    parent = StreetMaster.objects.get(id=parent_id)
    # print(parent)

    table_data = SurveyMaster.objects.get(id=id)

    form = SurveyMasterForm(instance=table_data)
    if request.method == 'POST':
        form = SurveyMasterForm(request.POST, instance=table_data)
        if form.is_valid():
            # print(form.cleaned_data)
            obj = form.save(commit=False)
            obj.dupcheck = f"{obj.lattitude}{obj.langitutte}"
            obj.street_master = parent

            try:
                obj.save()
                return redirect('child_stree_form', parent_id)
            except IntegrityError as e:
                messages.error(request, message="Data already exists.")
                form = SurveyMasterForm(instance=table_data)

        else:
            messages.error(request, message="Form is not valid")

    context = {"menu": "menu-street", "form": form, "parent": parent}
    return render(request, 'street/child_street_edit.html', context)


def delete_child_street(request, id, parent_id):
    # print(id)
    # print(parent_id)
    obj = SurveyMaster.objects.get(id=id)
    obj.delete()
    return redirect('child_stree_form', parent_id)


def edit_parent_street(request, id):
    obj = StreetMaster.objects.get(id=id)
    # print(obj)
    form = StreetForm(instance=obj)

    if request.method == 'POST':
        form = StreetForm(request.POST, instance=obj)

        if form.is_valid():
            obj = form.save(commit=False)
            dupcheck_value = f"{obj.river_name}{obj.block_name}{obj.sub_basin}{obj.district_name}{obj.town_name}{obj.taluk_name}"
            obj.dupcheck = dupcheck_value
            try:
                obj.save()
                obj = StreetMaster.objects.last()
                street_id = obj.id
                return redirect('child_stree_form', street_id)
            except IntegrityError as e:
                messages.error(request, message="Data already exists.")
        else:
            messages.error(request, message="Form is not valid")

    context = {"menu": "menu-street", "form": form}
    return render(request, 'street/edit_parent_street.html', context)


def exit_form(request):
    return redirect('list-of-street')


def new_street_edit(request, id):
    return redirect('child_stree_form', id)


def st_search_values(request):
    search_query = request.GET.get('search', '')
    # print(search_query)
    search_filter = (
            Q(river_name__list_of_values__icontains=search_query) |
            Q(block_name__list_of_values__icontains=search_query) |
            Q(sub_basin__list_of_values__icontains=search_query) |
            Q(district_name__list_of_values__icontains=search_query) |
            Q(town_name__list_of_values__icontains=search_query) |
            Q(taluk_name__list_of_values__icontains=search_query)
    )
    # print(search_filter)
    obj = StreetMaster.objects.filter(search_filter).order_by('river_name__list_of_values')
    # print(obj)

    context = {"menu": "menu-street", "obj": obj, "search_query": search_query}
    return render(request, 'street/street_list.html', context)


def street_excel(request):
    if request.method == 'POST':
        if 'upload_file' in request.FILES:
            upload_file = request.FILES['upload_file']

            upload_file_name = upload_file.name
            api_url = STREET_EXCEL_API_URL

            # Prepare the payload and files for the POST request
            payload = {}
            files = [('excel_file', (upload_file_name, upload_file.read(),
                                     'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))]
            headers = {}

            # Send the POST request to the API endpoint
            response = rq.request("POST", api_url, headers=headers, data=payload, files=files)
            # print(response.status_code)

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
                    messages.warning(request, message=response_data['error'])
                else:
                    messages.error(request, message="Unexpected response from the server")
            except ValueError:
                messages.error(request, message="Invalid JSON response from the server")

            return redirect('list-of-street')

    return HttpResponse("Invalid request method or file not provided")


def sample_excel_street(request):
    media_file_path = 'media/sample_excels/street_sample.xlsx'

    with open(media_file_path, 'rb') as file:
        response = HttpResponse(file.read(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="street_sample.xlsx"'
        return response