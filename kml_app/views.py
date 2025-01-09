import os

from django.contrib import messages
from django.core.serializers import serialize
from django.db import IntegrityError
from django.db.models import Q, ProtectedError
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.http import JsonResponse, HttpResponse
import json
import requests as rq
import configparser
import os

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'config.ini'))

ENCHROCHMENTS_EXCEL_API_URL = config['DEFAULT']['ENCHROCHMENTS_EXCEL_API_URL']


def cadastral_deviation_list(request):
    obj = CadastralDeviation.objects.all().order_by('unique_id')
    form = Ench_KMl_FORM()
    context = {"menu": "menu-dev", "obj": obj, "form": form}
    return render(request, 'cadastal_devaion/cadastal_devaion_list.html', context)


def kml_file_upload_ench(request):
    if request.method == "POST":
        file = request.FILES.get('kml_file')

        if not file:
            messages.error(request, "No file selected.")
            return redirect('deviation-list')

        allowed_types = ['.kml', '.kmz']

        if not any(file.name.endswith(ext) for ext in allowed_types):
            messages.error(request, "Only supports KML and KMZ file formats.")
            return redirect('deviation-list')
        else:
            form = Ench_KMl_FORM(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, message="KML or KMZ File successfully updated")
                return redirect('deviation-list')
            else:
                # print(form.errors)
                messages.error(request, "This River name  already KML File exists")
                return redirect('ench_kml_list')
    else:
        # Handle the case when the request method is not "POST"
        messages.error(request, "Invalid request method.")
        return redirect('deviation-list')


def ench_kml_edit(request, id):
    obj = EnchrochKMLTable.objects.get(id=id)
    form = Ench_KMl_FORM(instance=obj)
    if request.method == 'POST':
        file = request.FILES.get('kml_file')

        if not file:
            messages.error(request, "No file selected.")
            return redirect('ench_kml_edit', id)

        allowed_types = ['.kml', '.kmz']

        if not any(file.name.endswith(ext) for ext in allowed_types):
            messages.error(request, "Only supports KML and KMZ file formats.")
            return redirect('ench_kml_edit', id)
        else:
            form = Ench_KMl_FORM(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                form.save()
                messages.success(request, "KML or KMZ File successfully updated")
                return redirect('ench_kml_list')
            else:
                messages.error(request, "This River name already KML File exists")
                return redirect('ench_kml_list', id)
    # else:
    #     messages.error(request, "Invalid request method.")

    context = {"menu": "menu-dev", "form": form}
    return render(request, 'cadastal_devaion/intrusion_kml_edit.html', context)


def ench_kml_delete(request, id):
    obj = EnchrochKMLTable.objects.get(id=id)
    if request.method == 'POST':
        kml_file_path = obj.kml_file.path
        if os.path.exists(kml_file_path):
            os.remove(kml_file_path)

        obj.delete()
        return redirect('ench_kml_list')
    context = {"menu": "menu-dev", "obj": obj}

    return render(request, 'cadastal_devaion/ench_kml_delete.html', context)
def ench_kml_list(request):
    obj = EnchrochKMLTable.objects.all()
    context = {"menu": "menu-dev", "obj": obj}
    return render(request, 'cadastal_devaion/ench_kml_list.html', context)

def get_cadastral_value(request):
    # print("function working")
    if request.method == 'POST':
        data = json.loads(request.POST.get('output'))
        deviations = data.pop('deviations')

        # print(data)

        cad_obj = CadastralDeviation(**data)
        # print(cad_obj)
        cad_obj.save()
        # print(cad_obj.id)

        obj = CadastralDeviation.objects.last()
        for dev in deviations:
            dev_obj = DeviationValue(**dev, cadastral_deviation_id=obj.id)
            dev_obj.save()

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def get_cadastral_entry(request):
    # print("function working")
    cadastral_entry_id = request.GET.get('cadastral_pillar', None)
    # print(cadastral_entry_id)

    if cadastral_entry_id:
        cadastral_entry = CadastralEntry.objects.get(id=cadastral_entry_id)
        # print(cadastral_entry)
        # print(cadastral_entry.block_name)

        data = {
            'street': str(cadastral_entry.street),
            'ward': str(cadastral_entry.sub_bassin),
            'revenue_ward_no': str(cadastral_entry.r_ward),
            'town': str(cadastral_entry.town),
            'taluk': str(cadastral_entry.taluk),
            'district': str(cadastral_entry.district),
            'block_no': str(cadastral_entry.block),
            'tsno_sdno': str(cadastral_entry.tsno_sdno),
            'classify': str(cadastral_entry.classify),
            'sub_classify': str(cadastral_entry.sub_classify)
        }
        # print(data)
        return JsonResponse(data)
    else:
        return JsonResponse({})


def cadastral_entry_block_value(request):
    # print("function working")
    cadastral_master_id = request.GET.get('cadastral_master_id', None)
    # print(cadastral_entry_id)
    obj = CadastralMaster.objects.get(id=cadastral_master_id)
    if obj:
        # print(obj)
        table1_instance = CadastralMaster.objects.get(river_name=obj)
        # print("table1", table1_instance)
        table2_records = CadastralEntry.objects.filter(river_name=table1_instance)
        block_no_list = [record.block_no for record in table2_records]
        # print("block_no_list:", block_no_list)
        river_id = table1_instance.unique_id
        # print(river_id)

        data = {
            # "block_no_list": block_no_list,
            "river_id": river_id,
        }

        return JsonResponse(data)
    else:
        return JsonResponse({})


def block_no_click_autofill(request):
    # print("function working")
    block_no_value = request.GET.get('id_block_no', None)
    # print(block_no_value)
    obj = CadastralEntry.objects.get(block_no=block_no_value)
    # print(obj)
    if obj:

        data = {
            'tsno_sdno': str(obj.tsno_sdno),
            'classify': str(obj.classify),
            'sub_classify': str(obj.sub_classify),

        }

        return JsonResponse(data)
    else:
        return JsonResponse({})


def delete_cadastral_deviation(request, id):
    data = CadastralDeviation.objects.get(id=id)

    if request.method == 'POST':
        if data.upload_file:
            file_path = data.upload_file.path

            if os.path.exists(file_path):
                os.remove(file_path)
        try:
            data.delete()
        except ProtectedError as e:
            messages.error(request, message="You Can't Delete this Transaction Child Records  are Available")
        return redirect('deviation-list')

    context = {"menu": "menu-dev", "obj": data}
    return render(request, 'cadastal_devaion/cadastral_deviation_delete.html', context)


def file_upload(request, id):
    # print("working")
    # print(id)
    if request.method == "POST":
        file = request.FILES['upload_file']
        # print(file)
        obj = CadastralDeviation.objects.get(id=id)
        # print(obj)
        obj.upload_file = file
        obj.save()
        return redirect('deviation-list')


def edit_cadastral_deviation(request, id):
    # print(id)
    cadastral_deviation = CadastralDeviation.objects.get(id=id)

    remaining_cadastral_data = [{
        "no_of_buildings": cadastral_deviation.no_of_buildings,
        "no_of_floors": cadastral_deviation.no_of_floors,
        "usage_of_build": cadastral_deviation.usage_of_build,
        "occupier_name": cadastral_deviation.occupier_name,
        "enchorochment": cadastral_deviation.enchorochment,
        "river_instruction": cadastral_deviation.river_instruction,
        "hectare": cadastral_deviation.hectare,
        "area": cadastral_deviation.area,
        "sqm": cadastral_deviation.sqm,
        "remarks": cadastral_deviation.remarks,
        "asset_type": cadastral_deviation.asset_type,
        "buildings": cadastral_deviation.buildings,
    }]
    # print(remaining_cadastral_data)

    child_table_obj = DeviationValue.objects.filter(cadastral_deviation=cadastral_deviation)
    # print(child_table_obj)
    child_table = []

    for sub in child_table_obj:
        # Append the relevant data to the list
        child_table.append({
            'latitude': sub.latitude,
            'longitude': sub.longitude,
            'elevation': sub.elevation,
            'point_type': sub.point_type

        })
    # print(child_table)

    cadastral_deviation_form = CadastralDeviationForm(instance=cadastral_deviation)

    obj = ListOFValues.objects.filter(list_type__list_type='Point Type')
    point_type = []
    for item in obj:
        point_type.append(item)

    context = {"menu": "menu-dev", 'cadastral_deviation_form': cadastral_deviation_form,
               "obj_value": point_type, "child_table": child_table,
               "remaining_cadastral_data": remaining_cadastral_data, "id": id}
    return render(request, 'cadastal_devaion/edit_cadastral_deviation_form.html', context)


def edit_cadastral_deviation_json(request):
    if request.method == 'POST':
        data = json.loads(request.POST.get('output'))
        id = json.loads(request.POST.get('id'))
        # print(id)
        deviations = data.pop('deviations')

        old_obj = CadastralDeviation.objects.get(id=id)
        # print(old_obj)
        old_obj.delete()

        # print(data)

        cad_obj = CadastralDeviation(**data)
        # print(cad_obj)
        cad_obj.save()
        # print(cad_obj.id)

        obj = CadastralDeviation.objects.last()
        for dev in deviations:
            dev_obj = DeviationValue(**dev, cadastral_deviation_id=obj.id)
            dev_obj.save()

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


# ---------------------------------------------------------------------------------------------------

def cadastral_deviation_form(request):
    form = CadastralDeviationForm()

    if request.method == 'POST':
        form = NewEditCDForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            # print(len(form.cleaned_data))
            obj = form.save(commit=False)
            obj.dupcheck = f"{obj.unique_id}"
            obj.save()
            obj = CadastralDeviation.objects.last()
            parent_id = obj.id
            return redirect('child_enchrochment_form', parent_id)
        else:
            messages.error(request, message="Data already exists")
            form = CadastralDeviationForm()

    context = {"menu": "menu-dev", 'form': form}
    return render(request, 'cadastal_devaion/cadastral_deviation_form.html', context)


def child_enchrochment_form(request, id):
    parent = CadastralDeviation.objects.get(id=id)
    print(parent)
    obj = DeviationValue.objects.filter(cadastral_deviation=id)
    form = DeviationForm()
    form2 = DeviationForm2()


    if request.method == 'POST':
        form = DeviationForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            obj = form.save(commit=False)
            obj.cadastral_deviation = parent
            obj.dupcheck = f"{obj.latitude}{obj.longitude}"
            try:
                obj.save()
                return redirect('child_enchrochment_form', id)
            except IntegrityError as e:
                print(e)
                messages.error(request, message="Data already exists.")
                return redirect('child_enchrochment_form', id)
        else:
            messages.error(request, message="Form is not valid")

    context = {"menu": "menu-dev", "form": form, "form2": form2, "parent": parent, "obj": obj}
    return render(request, 'test.html', context)


def enchrochment2(request, id):
    if request.method == 'POST':
        parent = CadastralDeviation.objects.get(id=id)
        form = DeviationForm2(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            obj = form.save(commit=False)
            obj.dupcheck = f"{obj.latitude}{obj.longitude}"
            obj.cadastral_deviation = parent
            try:
                obj.save()
                return redirect('child_enchrochment_form', id)
            except IntegrityError as e:
                messages.error(request, message="Data already exists.")
                return redirect('child_enchrochment_form', id)
        else:
            messages.error(request, message="Form is not valid")


def child_enchrochment_edit_2(request, id, parent_id):
    # print(parent_id)
    # print(id)
    parent = CadastralDeviation.objects.get(id=parent_id)
    # print(parent)

    table_data = DeviationValue.objects.get(id=id)

    form = DeviationForm2(instance=table_data)
    if request.method == 'POST':
        form = DeviationForm2(request.POST, instance=table_data)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.dupcheck = f"{obj.latitude}{obj.longitude}"
            obj.cadastral_deviation = parent
            try:
                obj.save()
                return redirect('child_enchrochment_form', parent_id)
            except IntegrityError as e:
                messages.error(request, message="Data already exists.")
                form = DeviationForm2(instance=table_data)
        else:
            messages.error(request, message="Form is not valid")

    context = {"menu": "menu-dev", "form": form, "parent": parent}
    return render(request, 'test2.html', context)


def child_enchrochment_edit(request, id, parent_id):
    # print(parent_id)
    # print(id)
    parent = CadastralDeviation.objects.get(id=parent_id)
    # print(parent)

    table_data = DeviationValue.objects.get(id=id)

    form = DeviationForm(instance=table_data)
    if request.method == 'POST':
        form = DeviationForm(request.POST, instance=table_data)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.cadastral_deviation = parent
            obj.dupcheck = f"{obj.latitude}{obj.longitude}"
            try:
                obj.save()
                return redirect('child_enchrochment_form', parent_id)

            except IntegrityError as e:
                messages.error(request, message="Data already exists.")
                form = DeviationForm2(instance=table_data)
        else:
            messages.error(request, message="Form is not valid")

    context = {"menu": "menu-dev", "form": form, "parent": parent}
    return render(request, 'test2.html', context)


def delete_child_enchrochment(request, id, parent_id):
    # print(id)
    # print(parent_id)
    obj = DeviationValue.objects.get(id=id)
    obj.delete()
    # messages.error(request, "Delete successfully")
    return redirect('child_enchrochment_form', parent_id)


def edit_parent_enchrochment(request, id):
    obj = CadastralDeviation.objects.get(id=id)
    # print(obj)
    form = CadastralDeviationForm(instance=obj)

    if request.method == 'POST':
        form = NewEditCDForm(request.POST, instance=obj)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.dupcheck = f"{obj.unique_id}"
            obj.save()
            return redirect('child_enchrochment_form', id)
        else:
            messages.error(request, message="Data already exists")
            form = CadastralDeviationForm(instance=obj)

    context = {"menu": "menu-dev", "form": form, "obj": obj}
    return render(request, 'test3.html', context)


def exit_form(request):
    return redirect('deviation-list')


def new_enchrochment_edit(request, id):
    return redirect('child_enchrochment_form', id)


def get_point_id(request):
    if request.method == 'GET':
        point_id = request.GET.get('point_id', None)
        # print(point_id)
        obj = CadastralEntry.objects.get(id=point_id)

        data = {
            'latitude': obj.latitude,
            'longitude': obj.longitude,
            'elevation': obj.elevation,
        }

        # print(data)

        return JsonResponse(data)
    else:
        return JsonResponse({})


def get_En_survey_no(request):
    surveyNo = request.GET.get('surveyNo', None)
    if surveyNo:
        # print(type(surveyNo))
        obj = SurveyMaster.objects.filter(survey_no=surveyNo).first()
        # print(filter_obj)

        data = {
            'classification': obj.classification.list_of_values,
            'sub_classification': obj.sub_classification.list_of_values,
        }
        # print(data)
        return JsonResponse(data)
    else:
        return JsonResponse({})


def cd_search_values(request):
    search_query = request.GET.get('search', '')

    # print(search_query)
    search_filter = (
        Q(unique_id__icontains=search_query)

    )
    # print(search_filter)
    obj = CadastralDeviation.objects.filter(search_filter).order_by('unique_id')
    if not obj:
        search_filter = (

                Q(latitude__icontains=search_query) |
                Q(longitude__icontains=search_query)
        )

        query_set = DeviationValue.objects.filter(search_filter)
        # print(query_set)

        _id = []

        for obj in query_set:
            _id.append(obj.cadastral_deviation)
            # print(obj.cadastral_deviation)

        # print(_id)

        mastre_table = _id[0]
        # print(mastre_table.id)
        id = mastre_table.id

        obj = CadastralDeviation.objects.filter(id=id)

    context = {"menu": "menu-dev", "obj": obj, "search_query": search_query}
    return render(request, 'cadastal_devaion/cadastal_devaion_list.html', context)


def enchrochment_excel(request):
    if request.method == 'POST':
        if 'upload_file' in request.FILES:
            upload_file = request.FILES['upload_file']
            # print(upload_file)
            upload_file_name = upload_file.name

            api_url = ENCHROCHMENTS_EXCEL_API_URL

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

            return redirect('deviation-list')

    return HttpResponse("Invalid request method or file not provided")


def sample_excel_ench(request):
    media_file_path = 'media/sample_excels/ench.xlsx'

    with open(media_file_path, 'rb') as file:
        response = HttpResponse(file.read(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="enchrochments_sample.xlsx"'
        return response
