from django.db import IntegrityError
from django.shortcuts import render, redirect
from .models import WardRegion
from .forms import WardForm
from django.contrib import messages


def get_all_ward_data(request):
    obj = WardRegion.objects.all()
    context = {"menu": "menu-ward", "obj": obj}
    return render(request, 'ward/ward_list.html', context)


def new_ward_entry(request):
    form = WardForm()
    if request.method == 'POST':
        form = WardForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.ward_name = obj.ward_name.title()
            try:
                obj.save()
                return redirect('ward-all-data')
            except IntegrityError:
                messages.info(request, "Ward name already exists.")
        else:
            if 'ward_no' in form.errors:
                messages.info(request, "Ward no already exists.")
            if 'ward_name' in form.errors:
                messages.info(request, "Ward name already exists.")

            if 'ward_no' in form.errors and 'ward_name' in form.errors:
                messages.info(request, "Ward no already exists.")

            # messages.error(request, form.errors)

    context = {"menu": "menu-ward", "form": form}
    return render(request, 'ward/ward_form.html', context)


def edit_ward_entry(request, id):
    data = WardRegion.objects.get(id=id)
    form = WardForm(instance=data)

    if request.method == 'POST':
        form = WardForm(request.POST, instance=data)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.ward_name = obj.ward_name.title()
            try:
                obj.save()
                return redirect('ward-all-data')
            except IntegrityError:
                messages.info(request, "Ward name already exists.")
        else:
            if 'ward_no' in form.errors:
                messages.info(request, "Ward no already exists.")
            elif 'ward_name' in form.errors:
                messages.info(request, "Ward name already exists.")

    context = {"menu": "menu-ward", "form": form}
    return render(request, 'ward/ward_form.html', context)


def delete_ward_entry(request, id):
    data = WardRegion.objects.get(id=id)

    if request.method == 'POST':
        data.delete()
        return redirect('ward-all-data')

    context = {"menu": "menu-ward", "obj": data}
    return render(request, 'ward/ward_delete.html', context)
