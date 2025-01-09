import json
import os

from django.core.exceptions import MultipleObjectsReturned
from django.db.models.deletion import ProtectedError
from django.db import IntegrityError
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from kml import settings
from .models import *
from .forms import *
from django.contrib import messages
import requests as rq
import configparser
import os

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'config.ini'))

BOUNDARY_PILLAR_EXCEL_API_URL = config['DEFAULT']['BOUNDARY_PILLAR_EXCEL_API_URL']



def get_all_cadastral_entry(request):
    obj = CadastralEntry.objects.all().order_by('unique_id', 'latitude', 'longitude', 'remarks')
    form = Boundary_KMl_FORM()
    context = {"menu": "menu-cad", "obj": obj, "form": form}
    return render(request, 'cadastral_entry/cadastral_entry_list.html', context)


def get_cadastral_pillar(request):
    # print("function working")
    if request.method == 'POST':
        data = json.loads(request.POST.get('output'))
        # print(data)

        river_name_id = data['river_name_id']
        data['river_name_id'] = int(river_name_id)

        river_bank_values = data['river_bank_id']
        data['river_bank_id'] = int(river_bank_values)

        block_name_id = data['block_name_id']
        data['block_name_id'] = int(block_name_id)

        street_id = data['street_id']
        data['street_id'] = int(street_id)

        # print(data)

        obj = CadastralEntry(**data)
        # print(obj.cleaned_data)
        obj.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def edit_cadastral_pillar_json(request):
    if request.method == 'POST':
        data = json.loads(request.POST.get('output'))
        id = json.loads(request.POST.get('id'))
        # print(id)
        # print(data)

        river_name_id = data['river_name_id']
        data['river_name_id'] = int(river_name_id)

        river_bank_values = data['river_bank_id']
        data['river_bank_id'] = int(river_bank_values)

        block_no_id = data['block_no_id']
        data['block_no_id'] = int(block_no_id)

        previous_obj = CadastralEntry.objects.last()
        previous_obj.delete()

        obj = CadastralEntry(**data)
        # print(obj.cleaned_data)
        obj.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({})


def delete_cadastral_entry(request, id):
    data = CadastralEntry.objects.get(id=id)

    if request.method == 'POST':
        try:
            data.delete()
        except ProtectedError as e:
            messages.error(request, message="You Can't Delete this Transaction Child Records  are Available")

        return redirect('list-of-cadastral')

    context = {"menu": "menu-cad", "obj": data}
    return render(request, 'cadastral_entry/cadastral_delete.html', context)


def get_town_details_1(request):
    # print("function working")
    block_name = request.GET.get('block_name', None)
    river_name = request.GET.get('river', None)
    # print(block_name)
    if block_name and river_name:
        street = StreetMaster.objects.get(river_name__id=river_name, block_name__id=block_name)
        survey_table_data = list(street.surveymaster_set.all().values())
        non_dub = {i['street_name'] for i in survey_table_data}
        non_dub_list = list(non_dub)
        # block = BlockMaster.objects.get(id=block_name)
        # # print(block.id)
        # street_table = StreetMaster.objects.get(block_name=block.id)
        # # print(street_table)
        # survey_table = SurveyMaster.objects.filter(street_master=street_table.id)
        # # print(survey_table)
        # survey_table_data = list(survey_table.values())
        # # print(survey_table_data)
        #
        data = {
            'revenue_ward_no': street.revenue_ward_no,
            'taluk_name': str(street.taluk_name.list_of_values),
            'district_name': str(street.district_name.list_of_values),
            'sub_basin': str(street.sub_basin.list_of_values),
            'town_name': str(street.town_name.list_of_values),
            'survey_table_data': non_dub_list
        }
        return JsonResponse(data)
    return JsonResponse({})


def get_street_base(request):
    street_value = request.GET.get('street_value', None)
    # print(street_value)
    if street_value:
        survey_table = SurveyMaster.objects.get(street_name=street_value)
        # print(survey_table)

        data = {
            'survey_no': survey_table.survey_no,
            'classification': survey_table.classification,
            'sub_classification': survey_table.sub_classification,
            'langitutte': survey_table.langitutte,
            'lattitude': survey_table.lattitude,
        }
        # print(data)
        return JsonResponse(data)
    else:
        return JsonResponse({})


def photos_upload(request, id):
    objects = CadastralEntry.objects.get(id=id)

    pre_image = SubCadastralEntry.objects.filter(cadastral_entry=id)

    cadastral_entry = get_object_or_404(CadastralEntry, id=id)

    if request.method == 'POST':
        image = request.FILES['photos']
        allowed_types = ['image/jpeg', 'image/png']

        if image.content_type not in allowed_types:
            messages.info(request, "Only Support 'jpeg',  'png'")

        else:

            sub_cadastral_entry = SubCadastralEntry.objects.create(photos=image, cadastral_entry=cadastral_entry)
            sub_cadastral_entry_images = SubCadastralEntry.objects.filter(cadastral_entry=id)

            context = {"menu": "menu-cad", "obj": objects, "sub_cadastral_entry_images": sub_cadastral_entry_images}
            return render(request, 'cadastral_entry/photos_upload.html', context)

    context = {"menu": "menu-cad", "obj": objects, "pre_image": pre_image}
    return render(request, 'cadastral_entry/previous_image.html', context)


def get_blocks_for_river(request):
    river = request.GET.get('river', None)
    if river:
        streets = StreetMaster.objects.filter(river_name__id=river)
        blocks = [{
            "id": block.block_name.id,
            "value": block.block_name.list_of_values
        } for block in streets]
        return JsonResponse({"blocks": blocks})
    else:
        return JsonResponse({})


# ---------------------------------------------------------------------------------------------------


def get_street_value(request):
    street = request.GET.get('streetVal', None)
    if street:
        soNo_list = SurveyMaster.objects.filter(street_name=street)
        # print(len(soNo_list))

        list_data = []
        for soNo in soNo_list:
            list_data.append(soNo.survey_no)
        # print(len(list_data))

        survey_no = set(list_data)
        survey_no_list = list(survey_no)
        # print(street)

        data = {
            'soNo_list': survey_no_list,
        }
        # print(data)
        return JsonResponse(data)
    else:
        return JsonResponse({})


def get_survey_no(request):
    surveyNo = request.GET.get('surveyNo', None)
    if surveyNo:
        # print(type(surveyNo))
        filter_obj = SurveyMaster.objects.filter(survey_no=surveyNo)
        # print(filter_obj)

        list_data = []
        for obj in filter_obj:
            list_data.append(obj.lattitude)
        # print(list_data)

        data = {
            'latitude': list_data,
        }
        # print(data)
        return JsonResponse(data)
    else:
        return JsonResponse({})


def get_lat_no(request):
    lat = request.GET.get('lat', None)
    if lat:
        obj = SurveyMaster.objects.get(lattitude=lat)
        # print(obj)

        data = {
            'sub_classification': obj.sub_classification.list_of_values,
            'longitude': obj.langitutte,
            'classification': obj.classification.list_of_values,
        }

        # print(data)

        return JsonResponse(data)
    else:
        return JsonResponse({})


def get_CEntry_town_value(request):
    if request.method == 'GET':
        town = request.GET.get('town')
        # print(sub_bassinValue)
        street_master_table = StreetMaster.objects.filter(town_name__list_of_values=town)
        # print(street_master_table)

        block_list_data = []

        for block in street_master_table:
            block_list_data.append(block.block_name.list_of_values)

        data = {
            'block_list': block_list_data,

        }
        return JsonResponse(data)
    else:
        return JsonResponse({})


def get_CEntry_block_value(request):
    if request.method == 'GET':
        try:
            block = request.GET.get('block', None)
            town = request.GET.get('town', None)

            block_convert_title = block.lower()

            if block_convert_title in ["nan", "na", "none", None]:
                street_master_table = StreetMaster.objects.get(town_name__list_of_values=town)
            else:
                street_master_table = StreetMaster.objects.get(block_name__list_of_values=block)

            child_street_table = SurveyMaster.objects.filter(street_master=street_master_table.id)

            street_list_data = [subbas.street_name for subbas in child_street_table]
            street = list(set(street_list_data))

            data = {'street': street}
            return JsonResponse(data)

        except MultipleObjectsReturned as e:
            # print("Multiple objects returned:", e)
            street_master_table = StreetMaster.objects.get(town_name__list_of_values=town)
            child_street_table = SurveyMaster.objects.filter(street_master=street_master_table.id)

            street_list_data = [subbas.street_name for subbas in child_street_table]
            street = list(set(street_list_data))

            data = {'street': street}
            return JsonResponse(data)

        except Exception as e:
            # Handle any other exceptions
            print("Error:", e)
            return JsonResponse({'error': 'An error occurred while processing the request'})
    else:
        return JsonResponse({})


def new_cadastral_entry(request):
    # type_of_pillar = ListOFValues.objects.all()
    type_of_pillar = ListOFValues.objects.filter(
        list_type__list_type='Type Of Pillar'
    )
    # print(type_of_pillar)

    form = CadastralForm()

    if request.method == 'POST':
        form = EditCadastralForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            obj = form.save(commit=False)
            obj.dupcheck = f"{obj.unique_id}"

            obj.save()
            return redirect('list-of-cadastral')
        else:
            # print(form.errors)
            messages.error(request, message="Data already exists")
            form = CadastralForm(request.POST)

    context = {"menu": "menu-cad", "form": form, "type_of_pillar": type_of_pillar}
    return render(request, 'cadastral_entry/cadastral_entry_form.html', context)


def edit_cadastral_entry(request, id):
    type_of_pillar = ListOFValues.objects.filter(
        list_type__list_type='Type Of Pillar'
    )

    obj = CadastralEntry.objects.get(id=id)
    form = CadastralForm(instance=obj)
    if request.method == "POST":
        form = EditCadastralForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('list-of-cadastral')

    streets = StreetMaster.objects.filter(river_name__id=obj.river_name_id)
    blocks = [{
        "id": block.block_name.id,
        "value": block.block_name.list_of_values
    } for block in streets]

    street = StreetMaster.objects.get(river_name__id=obj.river_name_id, block_name__id=obj.block_name_id)
    streets_list = street.surveymaster_set.all().values()

    list_data = {
        'tsno_sdno': obj.tsno_sdno,
        'classify': obj.classify,
        'sub_classify': obj.sub_classify,
        'latitude': obj.latitude,
        'longitude': obj.longitude,
        'elevation': obj.elevation,
        'type_of_pillar': obj.type_of_pillar,
        'remarks': obj.remarks,
    }

    # print(data.unique_id)

    context = {
        "menu": "menu-cad",
        "form": form,
        "obj": list_data,
        "type_of_pillar": type_of_pillar,
        "id": id,
        "blocks": blocks,
        "streets_list": streets_list,
        's_river_id': obj.river_name_id,
        's_block_id': obj.block_name_id,
        's_street_id': obj.street,
        'object': obj
    }
    return render(request, 'cadastral_entry/edit_cadastral_entry_form.html', context)


def new_CEntry_edit(request, id):
    type_of_pillar = ListOFValues.objects.filter(
        list_type__list_type='Type Of Pillar'
    )

    obj = CadastralEntry.objects.get(id=id)
    # print(obj)
    form = CadastralForm(instance=obj)

    if request.method == 'POST':
        form = EditCadastralForm(request.POST, instance=obj)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.dupcheck = f"{obj.unique_id}"
            obj.save()
            return redirect('list-of-cadastral')
        else:
            messages.error(request, message="Data already exists")
            form = CadastralForm(instance=obj)

    context = {"menu": "menu-cad", "form": form, "edit_data": obj, 'type_of_pillar': type_of_pillar}
    return render(request, 'cadastral_entry/new_CEntry_edit.html', context)


def cn_delete_image(request, parent_id, id):
    photo = get_object_or_404(SubCadastralEntry, id=id)
    image_path = os.path.join(settings.MEDIA_ROOT, str(photo.photos))

    if os.path.exists(image_path):
        os.remove(image_path)

    photo.delete()
    return redirect('photos_upload', parent_id)


def ce_search_values(request):
    search_query = request.GET.get('search', '')

    # print(search_query)
    search_filter = (
            Q(unique_id__icontains=search_query) |
            Q(latitude__icontains=search_query) |
            Q(longitude__icontains=search_query)

    )
    # print(search_filter)
    obj = CadastralEntry.objects.filter(search_filter).order_by('unique_id')
    # print(obj)

    context = {"menu": "menu-cad", "obj": obj, "search_query": search_query}
    return render(request, 'cadastral_entry/cadastral_entry_list.html', context)


def cadastral_entry_excel(request):
    # print("function working")
    if request.method == 'POST':
        if 'upload_file' in request.FILES:
            upload_file = request.FILES['upload_file']
            # print(upload_file)
            upload_file_name = upload_file.name

            api_url = BOUNDARY_PILLAR_EXCEL_API_URL

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
            # except ValueError:
            #     messages.error(request, message="Invalid JSON response from the server")
            except ValueError as ve:
                error_message = f"ValueError occurred: {ve}"
                messages.error(request, message=error_message)

            return redirect('list-of-cadastral')

    return HttpResponse("Invalid request method or file not provided")


def sample_excel_BP(request):
    media_file_path = 'media/sample_excels/bounsample.xlsx'

    with open(media_file_path, 'rb') as file:
        response = HttpResponse(file.read(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="bondarypillar_sample.xlsx"'
        return response

def kml_file_upload_boundary(request):
    if request.method == "POST":
        file = request.FILES.get('kml_file')

        if not file:
            messages.error(request, "No file selected.")
            return redirect('list-of-cadastral')

        allowed_types = ['.kml', '.kmz']

        if not any(file.name.endswith(ext) for ext in allowed_types):
            messages.error(request, "Only supports KML and KMZ file formats.")
            return redirect('list-of-cadastral')
        else:
            form = Boundary_KMl_FORM(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, message="KML or KMZ File successfully updated")
                return redirect('list-of-cadastral')
            else:
                # print(form.errors)
                messages.error(request, "This River name  already KML File exists")
                return redirect('boundary_kml_list')
    else:
        # Handle the case when the request method is not "POST"
        messages.error(request, "Invalid request method.")
        return redirect('list-of-cadastral')


def boundary_kml_list(request):
    obj = BoundaryKMLTable.objects.all()
    context = {"menu": "menu-cad", "obj": obj}
    return render(request, 'cadastral_entry/boundary_kml_list.html', context)


def boundary_kml_edit(request, id):
    obj = BoundaryKMLTable.objects.get(id=id)
    form = Boundary_KMl_FORM(instance=obj)
    if request.method == 'POST':
        file = request.FILES.get('kml_file')

        if not file:
            messages.error(request, "No file selected.")
            return redirect('boundary_kml_edit', id)

        allowed_types = ['.kml', '.kmz']

        if not any(file.name.endswith(ext) for ext in allowed_types):
            messages.error(request, "Only supports KML and KMZ file formats.")
            return redirect('boundary_kml_edit', id)
        else:
            form = Intrusion_KMl_FORM(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                form.save()
                messages.success(request, "KML or KMZ File successfully updated")
                return redirect('boundary_kml_list')
            else:
                messages.error(request, "This River name already KML File exists")
                return redirect('boundary_kml_edit', id)
    # else:
    #     messages.error(request, "Invalid request method.")

    context = {"menu": "menu-cad", "form": form}
    return render(request, 'cadastral_entry/boundary_kml_edit.html', context)


def boundary_kml_delete(request, id):
    obj = BoundaryKMLTable.objects.get(id=id)
    if request.method == 'POST':
        kml_file_path = obj.kml_file.path
        if os.path.exists(kml_file_path):
            os.remove(kml_file_path)

        obj.delete()
        return redirect('boundary_kml_list')
    context = {"menu": "menu-cad", "obj": obj}

    return render(request, 'cadastral_entry/boundary_kml_delete.html', context)
