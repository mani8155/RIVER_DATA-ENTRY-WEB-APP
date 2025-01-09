from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import TownMaster, TalukMaster
from .forms import TownForm
from django.contrib import messages


def town_master_list(request):
    obj = TownMaster.objects.all()
    context = {"menu": "menu-town", "obj": obj}
    return render(request, 'town/town_list.html', context)


# def new_town_entry(request):
#     form = TownForm()
#     if request.method == 'POST':
#         form = TownForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('list-of-town')
#     context = {"menu": "menu-town", "form": form}
#     return render(request, 'town/town_form.html', context)


def new_town_entry(request):
    form = TownForm()
    if request.method == 'POST':
        form = TownForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.town_name = obj.town_name.title()
            rev_ward_no = obj.revenue_division_no
            # obj.revenue_division_name = obj.revenue_division_name.title()

            obj.dupcheck = f"{rev_ward_no}{obj.town_name}{obj.taluk_name}{obj.district_name}"

            validation = TownMaster.objects.filter(dupcheck=obj.dupcheck)

            if validation:
                messages.info(request, 'This data already exists.')
            else:
                obj.save()
                return redirect('list-of-town')

    context = {"menu": "menu-town", "form": form}
    return render(request, 'town/town_form.html', context)


def edit_town_entry(request, id):
    data = TownMaster.objects.get(id=id)
    form = TownForm(instance=data)

    if request.method == 'POST':
        form = TownForm(request.POST, instance=data)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.town_name = obj.town_name.title()
            rev_ward_no = obj.revenue_division_no
            # obj.revenue_division_name = obj.revenue_division_name.title()

            obj.dupcheck = f"{rev_ward_no}{obj.town_name}{obj.taluk_name}{obj.district_name}"

            validation = TownMaster.objects.get(dupcheck=obj.dupcheck)

            if validation and validation.id != id:
                messages.info(request, 'This data already exists.')
            else:
                obj.save()
                return redirect('list-of-town')

    context = {"menu": "menu-town", "form": form}
    return render(request, 'town/town_form.html', context)


def delete_town(request, id):
    data = TownMaster.objects.get(id=id)

    if request.method == 'POST':
        data.delete()
        return redirect('list-of-town')

    context = {"menu": "menu-town", "obj": data}
    return render(request, 'town/town_delete.html', context)


def get_ward(request):
    print("function working")
    id_taluk_name = request.GET.get('id_taluk_name')
    print(id_taluk_name)
    if id_taluk_name:
        street = TalukMaster.objects.get(id=id_taluk_name)
        # print(street)
        # print(street.town_name)

        data = {
            'ward_name': str(street.ward_name),

        }
        print(data)
        return JsonResponse(data)
    else:
        return JsonResponse({})