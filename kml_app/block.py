from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import BlockMaster, TownMaster
from .forms import WardForm, BlockForm
from django.contrib import messages


def get_all_block_data(request):
    obj = BlockMaster.objects.all()
    context = {"menu": "menu-block", "obj": obj}
    return render(request, 'block/block_list.html', context)


def block_form(request):
    form = BlockForm()
    if request.method == 'POST':
        form = BlockForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.block_name = obj.block_name.title()
            obj.save()
            return redirect('block-lists')

    context = {"menu": "menu-block", "form": form}
    return render(request, 'block/block_form.html', context)


def block_edit_entry(request, id):
    data = BlockMaster.objects.get(id=id)
    form = BlockForm(instance=data)

    if request.method == 'POST':
        form = BlockForm(request.POST, instance=data)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.block_name = obj.block_name.title()
            obj.save()
            return redirect('block-lists')

    context = {"menu": "menu-block", "form": form}
    return render(request, 'block/block_form.html', context)


def delete_block(request, id):
    data = BlockMaster.objects.get(id=id)

    if request.method == 'POST':
        data.delete()
        return redirect('block-lists')

    context = {"menu": "menu-block", "obj": data}
    return render(request, 'block/block_delete.html', context)


def get_town_data(request):
    # print("function working")
    town_name = request.GET.get('town_name', None)
    if town_name:
        town = TownMaster.objects.get(id=town_name)
        data = {
            'revenue_division_no': town.revenue_division_no,
            'taluk_name': str(town.taluk_name),
            'district_name': str(town.district_name),
            'ward_name': str(town.ward_name),
        }
        print(data)
        return JsonResponse(data)
    else:
        return JsonResponse({})
