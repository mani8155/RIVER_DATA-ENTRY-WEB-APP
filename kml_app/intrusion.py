from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Q, ProtectedError
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.http import HttpResponse
import requests as rq
import configparser
import os

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'config.ini'))

INTRUSION_EXCEL_API_URL = config['DEFAULT']['INTRUSION_EXCEL_API_URL']


def intrusion_list(request):
    obj = IntrusionMaster.objects.all().order_by('unique_id')
    form = Intrusion_KMl_FORM()

    context = {"menu": "menu-intrusion", "obj": obj, "form": form}
    return render(request, 'intrusion_master/intrusion_list.html', context)


def kml_file_upload_intrusion(request):
    if request.method == "POST":
        file = request.FILES.get('kml_file')

        if not file:
            messages.error(request, "No file selected.")
            return redirect('intrusion_list')

        allowed_types = ['.kml', '.kmz']

        if not any(file.name.endswith(ext) for ext in allowed_types):
            messages.error(request, "Only supports KML and KMZ file formats.")
            return redirect('intrusion_list')
        else:
            form = Intrusion_KMl_FORM(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, message="KML or KMZ File successfully updated")
                return redirect('intrusion_list')
            else:
                # print(form.errors)
                messages.error(request, "This River name  already KML File exists")
                return redirect('intrusion_kml_list')
    else:
        # Handle the case when the request method is not "POST"
        messages.error(request, "Invalid request method.")
        return redirect('intrusion_list')


def intrusion_kml_list(request):
    obj = IntrusionKMLTable.objects.all()
    context = {"menu": "menu-intrusion", "obj": obj}
    return render(request, 'intrusion_master/intrusion_kml_list.html', context)


def intrusion_kml_edit(request, id):
    obj = IntrusionKMLTable.objects.get(id=id)
    form = Intrusion_KMl_FORM(instance=obj)
    if request.method == 'POST':
        file = request.FILES.get('kml_file')

        if not file:
            messages.error(request, "No file selected.")
            return redirect('intrusion_kml_edit', id)

        allowed_types = ['.kml', '.kmz']

        if not any(file.name.endswith(ext) for ext in allowed_types):
            messages.error(request, "Only supports KML and KMZ file formats.")
            return redirect('intrusion_kml_list', id)
        else:
            form = Intrusion_KMl_FORM(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                form.save()
                messages.success(request, "KML or KMZ File successfully updated")
                return redirect('intrusion_kml_list')
            else:
                messages.error(request, "This River name already KML File exists")
                return redirect('intrusion_kml_list', id)
    # else:
    #     messages.error(request, "Invalid request method.")

    context = {"menu": "menu-intrusion", "form": form}
    return render(request, 'intrusion_master/intrusion_kml_edit.html', context)


def intrusion_kml_delete(request, id):
    obj = IntrusionKMLTable.objects.get(id=id)
    if request.method == 'POST':
        kml_file_path = obj.kml_file.path
        if os.path.exists(kml_file_path):
            os.remove(kml_file_path)

        obj.delete()
        return redirect('intrusion_kml_list')
    context = {"menu": "menu-intrusion", "obj": obj}

    return render(request, 'intrusion_master/intrusion_kml_delete.html', context)


def intrusion_form(request):
    form = IntrusionForm()

    if request.method == 'POST':
        form = EditIntrusionForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            obj = form.save(commit=False)
            obj.dupcheck = f"{obj.unique_id}"
            obj.save()
            obj = IntrusionMaster.objects.last()
            parent_id = obj.id
            return redirect('child_intrusion_form', parent_id)
        else:
            messages.error(request, message="Data already exists")
            form = IntrusionForm()

    context = {"menu": "menu-intrusion", 'form': form}
    return render(request, 'intrusion_master/intrusion_form.html', context)


def child_intrusion_form(request, id):
    parent = IntrusionMaster.objects.get(id=id)
    obj = IntrusionChild.objects.filter(intrusion_master=id)
    form = IntrusionChildForm()
    form2 = IntrusionChildForm2()

    if request.method == 'POST':
        form = IntrusionChildForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            obj = form.save(commit=False)
            obj.intrusion_master = parent
            obj.dupcheck = f"{obj.latitude}{obj.longitude}"
            try:
                obj.save()
                return redirect('child_intrusion_form', id)
            except IntegrityError as e:
                messages.error(request, message="Data already exists.")
                return redirect('child_intrusion_form', id)
        else:
            messages.error(request, message="Form is not valid")

    context = {"menu": "menu-intrusion", "form": form, "form2": form2, "parent": parent, "obj": obj}
    return render(request, 'intrusion_master/child_intrusion_form.html', context)


def child_intrusion_form2(request, id):
    if request.method == 'POST':
        parent = IntrusionMaster.objects.get(id=id)
        form = IntrusionChildForm2(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            obj = form.save(commit=False)
            obj.intrusion_master = parent
            obj.dupcheck = f"{obj.latitude}{obj.longitude}"
            try:
                obj.save()
                return redirect('child_intrusion_form', id)
            except IntegrityError as e:
                messages.error(request, message="Data already exists.")
                return redirect('child_intrusion_form', id)
        else:
            messages.error(request, message="Form is not valid")


def child_intrusion_edit(request, id, parent_id):
    # print(parent_id)
    # print(id)
    parent = IntrusionMaster.objects.get(id=parent_id)
    # print(parent)

    table_data = IntrusionChild.objects.get(id=id)

    form = IntrusionChildForm(instance=table_data)
    if request.method == 'POST':
        form = IntrusionChildForm(request.POST, instance=table_data)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.intrusion_master = parent
            obj.dupcheck = f"{obj.latitude}{obj.longitude}"

            try:
                obj.save()
                return redirect('child_intrusion_form', parent_id)
            except IntegrityError as e:
                messages.error(request, message="Data already exists.")
                form = IntrusionChildForm(instance=table_data)
        else:
            messages.error(request, message="Form is not valid")

    context = {"menu": "menu-intrusion", "form": form, "parent": parent}
    return render(request, 'test2.html', context)


def child_intrusion_edit_2(request, id, parent_id):
    # print(parent_id)
    # print(id)
    parent = IntrusionMaster.objects.get(id=parent_id)
    # print(parent)

    table_data = IntrusionChild.objects.get(id=id)

    form = IntrusionChildForm2(instance=table_data)
    if request.method == 'POST':
        form = IntrusionChildForm2(request.POST, instance=table_data)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.intrusion_master = parent
            obj.dupcheck = f"{obj.latitude}{obj.longitude}"

            try:
                obj.save()
                return redirect('child_intrusion_form', parent_id)
            except IntegrityError as e:
                messages.error(request, message="Data already exists.")
                form = IntrusionChildForm2(instance=table_data)
        else:
            messages.error(request, message="Form is not valid")

    context = {"menu": "menu-intrusion", "form": form, "parent": parent}
    return render(request, 'test2.html', context)


def delete_child_intrusion(request, id, parent_id):
    # print(id)
    # print(parent_id)
    obj = IntrusionChild.objects.get(id=id)
    obj.delete()
    # messages.error(request, "Delete successfully")
    return redirect('child_intrusion_form', parent_id)


def edit_parent_intrusion(request, id):
    obj = IntrusionMaster.objects.get(id=id)
    # print(obj)
    form = IntrusionForm(instance=obj)

    if request.method == 'POST':
        form = EditIntrusionForm(request.POST, instance=obj)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.dupcheck = f"{obj.unique_id}"
            obj.save()
            return redirect('child_intrusion_form', id)
        else:
            messages.error(request, message="Data already exists")
            form = IntrusionForm(instance=obj)

    context = {"menu": "menu-intrusion", "form": form, "obj": obj}
    return render(request, 'test3.html', context)


def intrusion_exit_form(request):
    return redirect('intrusion_list')


def delete_intrusion(request, id):
    data = IntrusionMaster.objects.get(id=id)

    if request.method == 'POST':
        if data.upload_file:
            file_path = data.upload_file.path

            if os.path.exists(file_path):
                os.remove(file_path)
        try:
            data.delete()
        except ProtectedError as e:
            messages.error(request, message="You Can't Delete this Transaction Child Records  are Available")
        return redirect('intrusion_list')

    context = {"menu": "menu-intrusion", "obj": data}
    return render(request, 'cadastal_devaion/cadastral_deviation_delete.html', context)


def intrusion_search_values(request):
    search_query = request.GET.get('search', '')

    # print(search_query)
    search_filter = (
        Q(unique_id__icontains=search_query)

    )
    # print(search_filter)
    obj = IntrusionMaster.objects.filter(search_filter).order_by('unique_id')
    if not obj:
        search_filter = (

                Q(latitude__icontains=search_query) |
                Q(longitude__icontains=search_query)
        )

        query_set = IntrusionChild.objects.filter(search_filter)
        # print(query_set)

        _id = []

        for obj in query_set:
            _id.append(obj.intrusion_master)
            # print(obj.cadastral_deviation)

        # print(_id)

        mastre_table = _id[0]
        # print(mastre_table.id)
        id = mastre_table.id

        obj = IntrusionMaster.objects.filter(id=id)

    context = {"menu": "menu-intrusion", "obj": obj, "search_query": search_query}
    return render(request, 'intrusion_master/intrusion_list.html', context)


def intrusion_excel(request):
    if request.method == 'POST':
        if 'upload_file' in request.FILES:
            upload_file = request.FILES['upload_file']
            # print(upload_file)
            upload_file_name = upload_file.name

            api_url = INTRUSION_EXCEL_API_URL
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

            return redirect('intrusion_list')

    return HttpResponse("Invalid request method or file not provided")


def sample_excel_intr(request):
    media_file_path = 'media/sample_excels/intr.xlsx'

    with open(media_file_path, 'rb') as file:
        response = HttpResponse(file.read(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="intrusion_sample.xlsx"'
        return response

