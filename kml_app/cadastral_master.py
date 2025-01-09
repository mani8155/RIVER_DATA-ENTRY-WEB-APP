import json
import requests as rq
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Q, ProtectedError
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
import configparser
import os

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'config.ini'))

CADASTRAL_LINE_EXCEL_API_URL = config['DEFAULT']['CADASTRAL_LINE_EXCEL_API_URL']


def cadastralmaster_entrys(request):
    obj = CadastralMaster.objects.all().order_by('unique_id', 'river_name')
    form = CM_KMl_FORM()
    context = {"menu": "menu-cadmas", "obj": obj, "form": form}
    return render(request, 'cadastral_master/cadastral_master_list.html', context)


def new_cadastralmaster_entry(request):
    form = CadastralMasterForm()

    ward_lists = WardRegion.objects.all()

    # street_list = SurveyMaster.objects.all()

    context = {"menu": "menu-cadmas", "form": form, "ward_lists": ward_lists}
    return render(request, 'cadastral_master/cadastral_master_form.html', context)


def delete_cadastral_master(request, id):
    data = CadastralMaster.objects.get(id=id)

    if request.method == 'POST':
        try:
            data.delete()
        except ProtectedError as e:
            messages.error(request, message="You Can't Delete this Transaction Child Records  are Available")

        return redirect('cadastral-master')

    context = {"menu": "menu-cadmas", "obj": data}
    return render(request, 'cadastral_master/cadastral_delete.html', context)


def cl_kml_list(request):
    obj = CadastralMasterKMLTable.objects.all()
    context = {"menu": "menu-cadmas", "obj": obj}
    return render(request, 'cadastral_master/kml_list.html', context)


def cl_kml_edit(request, id):
    obj = CadastralMasterKMLTable.objects.get(id=id)
    form = CM_KMl_FORM(instance=obj)
    if request.method == 'POST':
        file = request.FILES.get('kml_file')

        if not file:
            messages.error(request, "No file selected.")
            return redirect('cl_kml_edit', id)

        allowed_types = ['.kml', '.kmz']

        if not any(file.name.endswith(ext) for ext in allowed_types):
            messages.error(request, "Only supports KML and KMZ file formats.")
            return redirect('cl_kml_edit', id)
        else:
            form = CM_KMl_FORM(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                form.save()
                messages.success(request, "KML or KMZ File successfully updated")
                return redirect('cl_kml_list')
            else:
                messages.error(request, "This River name already KML File exists")
                return redirect('cl_kml_edit', id)
    # else:
    #     messages.error(request, "Invalid request method.")

    context = {"menu": "menu-cadmas", "form": form}
    return render(request, 'cadastral_master/cl_kml_edit.html', context)


def cl_kml_delete(request, id):
    obj = CadastralMasterKMLTable.objects.get(id=id)
    if request.method == 'POST':
        kml_file_path = obj.kml_file.path
        if os.path.exists(kml_file_path):
            os.remove(kml_file_path)

        obj.delete()
        return redirect('cl_kml_list')
    context = {"menu": "menu-cadmas", "obj": obj}

    return render(request, 'cadastral_master/cl_kml_delete.html', context)


def cl_kml_search_values(request):
    search_query = request.GET.get('search', '').title()

    # print(search_query)
    search_filter = (
        Q(river_name__list_of_values__icontains=search_query)
    )
    # print(search_filter)
    obj = CadastralMasterKMLTable.objects.filter(search_filter).order_by('river_name')
    # print(obj)

    context = {"menu": "menu-cadmas", "obj": obj, "search_query": search_query}
    return render(request, 'cadastral_master/kml_list.html', context)


def file_upload_master(request):
    if request.method == "POST":
        file = request.FILES.get('kml_file')

        if not file:
            messages.error(request, "No file selected.")
            return redirect('cadastral-master')

        allowed_types = ['.kml', '.kmz']

        if not any(file.name.endswith(ext) for ext in allowed_types):
            messages.error(request, "Only supports KML and KMZ file formats.")
            return redirect('cadastral-master')
        else:
            form = CM_KMl_FORM(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, message="KML or KMZ File successfully updated")
                return redirect('cadastral-master')
            else:
                # print(form.errors)
                messages.error(request, "This River name  already KML File exists")
                return redirect('cl_kml_list')
    else:
        # Handle the case when the request method is not "POST"
        messages.error(request, "Invalid request method.")
        return redirect('cadastral-master')


def sub_cadastal_line(request):
    # print("function working")
    if request.method == 'POST':
        data = json.loads(request.POST.get('output'))
        deviations = data.pop('deviations')

        # print(data)
        # print(deviations)

        cad_line = CadastralMasterForm(data)
        cad_line.save()

        obj = CadastralMaster.objects.last()
        # print("obj", obj.id)
        for dev in deviations:
            # print("loop working")

            dev_obj = SubCadastralLine(**dev, cadastral_id=obj.id)
            dev_obj.save()

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def edit_cadastramaster_entry(request, id):
    data = CadastralMaster.objects.get(id=id)

    sub_cadastral_lines = SubCadastralLine.objects.filter(cadastral=data)

    sub_cadastral_data_list = []

    for sub_cadastral_line in sub_cadastral_lines:
        # Append the relevant data to the list
        sub_cadastral_data_list.append({
            'ward': sub_cadastral_line.ward,
            'taluk': sub_cadastral_line.taluk,
            'town': sub_cadastral_line.town,
            'block': sub_cadastral_line.block,
            'lat': sub_cadastral_line.lat,
            'long': sub_cadastral_line.long,

        })

    # print(sub_cadastral_data_list)
    ward_lists = WardRegion.objects.all()

    deviations = sub_cadastral_data_list

    form = CadastralMasterForm(instance=data)

    context = {"menu": "menu-cadmas", "form": form, "sub_cadastral_data_list": sub_cadastral_data_list,
               "ward_lists": ward_lists, "id": id}
    return render(request, 'cadastral_master/edit_cadastral_master_form.html', context)


def edit_cadastramaster_form_json(request):
    # print("edit_cadastramaster_form_json ")
    if request.method == 'POST':
        data = json.loads(request.POST.get('output'))
        id = json.loads(request.POST.get('id'))
        # print(data)
        deviations = data.pop('deviations')
        # print(data)
        # print(deviations)

        previous_data = CadastralMaster.objects.get(id=id)
        # print(previous_data)
        previous_data.delete()

        cad_line = CadastralMasterForm(data)
        cad_line.save()

        obj = CadastralMaster.objects.last()
        # print("obj", obj.id)
        # print(deviations)
        for dev in deviations:
            # print("loop working")
            dev_obj = SubCadastralLine(**dev, cadastral_id=obj.id)
            dev_obj.save()

        return JsonResponse({'status': 'success'})

    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def get_ward_cadastral_master(request):
    if request.method == 'GET':
        data = request.GET.get('selected_value', )
        # print(data)

        try:
            ward_name = StreetMaster.objects.get(ward_name=data)
            # print(ward_name.block_name)

            data = {
                'block_name': str(ward_name.block_name)
            }

            return JsonResponse(data)

        except ObjectDoesNotExist:
            # print("StreetMaster not found for ward_name:", data)
            data = {
                'block_name': ""
            }
            return JsonResponse(data)
    else:
        return JsonResponse({})


def block_use_get_data(request):
    # print("block_use_get_data working")
    if request.method == 'GET':
        data = request.GET.get('selected_value', )

        block_instance = BlockMaster.objects.get(block_name=data)
        street = StreetMaster.objects.get(block_name=block_instance)

        # print(street)
        # print(street.id)
        # print(street.town_name)
        # print(street.taluk_name)

        sub_table = SurveyMaster.objects.filter(street_master=street.id)
        sub_table_data = list(sub_table.values())

        data = {
            'town_name': str(street.town_name),
            'taluk_name': str(street.taluk_name),
            'sub_table': sub_table_data,
        }
        # print(data)

        return JsonResponse(data)
    else:
        return JsonResponse({})


def longitude_get_data(request):
    if request.method == 'GET':
        data = request.GET.get('selected_value', )
        # print(data)

        obj = SurveyMaster.objects.get(lattitude=data)
        # print(obj)

        data = {
            'langitutte': str(obj.langitutte),
        }
        # print(data)

        return JsonResponse(data)
    else:
        return JsonResponse({})


# -----------------------------------------------------------------------------------------------------

def new_cm_form(request):
    form = CadastralMasterForm()

    if request.method == 'POST':
        form = NewEditCadastralMasterForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            obj = form.save(commit=False)
            obj.dupcheck = f"{obj.river_name}{obj.taluk}{obj.block}{obj.district}{obj.town}{obj.sub_bassin}{obj.unique_id}"

            obj.save()

            obj2 = CadastralMaster.objects.last()
            id = obj2.id

            return redirect('child_cm_master_form', id)

        else:
            print(form.errors)
            messages.error(request, message="Data already exists")
            form = CadastralMasterForm()

    context = {"menu": "menu-cadmas", "form": form}
    return render(request, 'cadastral_master/new_cm_form.html', context)


def get_cm_river_value(request):
    if request.method == 'GET':
        rivValue = request.GET.get('rivValue', )
        river_name = ListOFValues.objects.get(id=rivValue)

        street_master = StreetMaster.objects.filter(river_name=river_name)

        list_data = []

        for subbas in street_master:
            list_data.append(subbas.sub_basin.list_of_values)

        not_allow_dub = set(list_data)
        sub_bassin = list(not_allow_dub)
        # print(sub_bassin)

        data = {
            'sub_bassin': sub_bassin,
        }
        # print(data)
        return JsonResponse(data)
    else:
        return JsonResponse({})


def get_cm_subbassin_value(request):
    if request.method == 'GET':
        sub_bassinValue = request.GET.get('sub_bassinVal', )
        # print(sub_bassinValue)
        street_master_table = StreetMaster.objects.filter(sub_basin__list_of_values=sub_bassinValue)
        # print(street_master_table)

        list_data = []

        for subbas in street_master_table:
            list_data.append(subbas.district_name.list_of_values)
        # print(list_data)

        not_allow_dub = set(list_data)
        district = list(not_allow_dub)
        # print(sub_bassin)

        data = {
            'district': district,
        }
        # print(data)
        return JsonResponse(data)
    else:
        return JsonResponse({})


def get_cm_dist_value(request):
    if request.method == 'GET':
        dist = request.GET.get('dist', )
        # print(sub_bassinValue)
        street_master_table = StreetMaster.objects.filter(district_name__list_of_values=dist)
        # print(street_master_table)

        list_data = []

        for subbas in street_master_table:
            list_data.append(subbas.taluk_name.list_of_values)
        # print(list_data)

        not_allow_dub = set(list_data)
        taluk = list(not_allow_dub)
        # print(sub_bassin)

        data = {
            'taluk': taluk,
        }
        # print(data)
        return JsonResponse(data)
    else:
        return JsonResponse({})


def get_cm_taluk_value(request):
    if request.method == 'GET':
        taluk = request.GET.get('taluk', )
        # print(sub_bassinValue)
        street_master_table = StreetMaster.objects.filter(taluk_name__list_of_values=taluk)
        # print(street_master_table)

        list_data = []

        for subbas in street_master_table:
            list_data.append(subbas.town_name.list_of_values)
        # print(list_data)

        not_allow_dub = set(list_data)
        town = list(not_allow_dub)
        # print(sub_bassin)

        data = {
            'town': town,
        }
        # print(data)
        return JsonResponse(data)
    else:
        return JsonResponse({})


def get_cm_town_value(request):
    if request.method == 'GET':
        town = request.GET.get('town', )
        # print(sub_bassinValue)
        street_master_table = StreetMaster.objects.get(town_name__list_of_values=town)
        # print(street_master_table.id)

        #     list_data = []
        #
        #     for subbas in street_master_table:
        #         list_data.append(subbas.town_name.list_of_values)
        #     # print(list_data)
        #
        #     not_allow_dub = set(list_data)
        #     town = list(not_allow_dub)
        #     # print(sub_bassin)
        #
        data = {
            'block': street_master_table.block_name.list_of_values,
        }
        # print(data)
        return JsonResponse(data)
    else:
        return JsonResponse({})


def child_cm_master_form(request, id):
    # print(id)
    parent = CadastralMaster.objects.get(id=id)
    obj = SubCadastralLine.objects.filter(cadastral=id)
    form = SubCadastralLineForm()

    if request.method == 'POST':
        form = SubCadastralLineForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            obj = form.save(commit=False)
            obj.cadastral = parent
            obj.dupcheck = f"{obj.lat}{obj.long}"
            try:
                obj.save()
                return redirect('child_cm_master_form', id)
            except IntegrityError as e:
                messages.error(request, message="Data already exists.")
                return redirect('child_cm_master_form', id)

        else:
            messages.error(request, message="Form is not valid")

    context = {"menu": "menu-cadmas", "form": form, "parent": parent, "obj": obj}
    return render(request, 'cadastral_master/child_street_master_form.html', context)


def child_new_cm_edit(request, id, parent_id):
    # print(parent_id)
    # print(id)
    parent = CadastralMaster.objects.get(id=parent_id)
    # print(parent)

    table_data = SubCadastralLine.objects.get(id=id)

    form = SubCadastralLineForm(instance=table_data)
    if request.method == 'POST':
        form = SubCadastralLineForm(request.POST, instance=table_data)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.cadastral = parent
            obj.dupcheck = f"{obj.lat}{obj.long}"

            try:
                obj.save()
                return redirect('child_cm_master_form', parent_id)

            except IntegrityError as e:
                messages.error(request, message="Data already exists.")
                form = SubCadastralLineForm(instance=table_data)

        else:
            messages.error(request, message="Form is not valid")

    context = {"menu": "menu-cadmas", "form": form, "parent": parent}
    return render(request, 'cadastral_master/child_new_cm_edit.html', context)


def delete_new_cm_child(request, id, parent_id):
    # print(id)
    # print(parent_id)
    obj = SubCadastralLine.objects.get(id=id)
    obj.delete()
    return redirect('child_cm_master_form', parent_id)


def edit_parent_new_cm(request, id):
    obj = CadastralMaster.objects.get(id=id)
    # print(obj)
    form = CadastralMasterForm(instance=obj)

    if request.method == 'POST':
        form = NewEditCadastralMasterForm(request.POST, instance=obj)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.dupcheck = f"{obj.river_name}{obj.taluk}{obj.block}{obj.district}{obj.town}{obj.sub_bassin}{obj.unique_id}"
            obj.save()
            return redirect('child_cm_master_form', id)

        else:
            form = CadastralMasterForm(request.POST, instance=obj)
            messages.error(request, message="Data already exists ")

    context = {"menu": "menu-cadmas", "form": form, "obj": obj}
    return render(request, 'cadastral_master/edit_parent_cm_form.html', context)


def exit_new_cm(request):
    return redirect('cadastral-master')


def new_cm_edit(request, id):
    return redirect('child_cm_master_form', id)


def cm_search_values(request):
    search_query = request.GET.get('search', '').title()

    # print(search_query)
    search_filter = (
            Q(river_name__list_of_values__icontains=search_query) |
            Q(unique_id__icontains=search_query)
    )
    # print(search_filter)
    obj = CadastralMaster.objects.filter(search_filter).order_by('unique_id')
    # print(obj)

    context = {"menu": "menu-cadmas", "obj": obj, "search_query": search_query}
    return render(request, 'cadastral_master/cadastral_master_list.html', context)


def cadastral_excel(request):
    if request.method == 'POST':
        if 'upload_file' in request.FILES:
            upload_file = request.FILES['upload_file']
            # print(upload_file)
            upload_file_name = upload_file.name

            api_url = CADASTRAL_LINE_EXCEL_API_URL

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

            return redirect('cadastral-master')

    return HttpResponse("Invalid request method or file not provided")


def sample_excel_CL(request):
    media_file_path = 'media/sample_excels/cadasline.xlsx'

    with open(media_file_path, 'rb') as file:
        response = HttpResponse(file.read(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="cadastral_line.xlsx"'
        return response