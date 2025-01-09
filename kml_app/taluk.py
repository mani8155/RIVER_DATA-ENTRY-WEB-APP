from django.shortcuts import render, redirect
from .models import TalukMaster
from .forms import TalukForm
from django.contrib import messages


def taluk_list(request):
    obj = TalukMaster.objects.all()
    context = {"menu": "menu-taluk", "obj": obj}
    return render(request, 'taluk/taluk_list.html', context)


def new_taluk_entry(request):
    form = TalukForm()
    if request.method == 'POST':
        form = TalukForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.taluk_name = obj.taluk_name.title()
            ward_name = obj.ward_name
            # print(ward_name)

            obj.dupcheck = f"{obj.taluk_name}{ward_name}"
            validation = TalukMaster.objects.filter(dupcheck=obj.dupcheck)
            if validation:
                messages.info(request, "This data already exists.")
                # obj.delete()
            else:
                # print("Not dublicate")
                obj.save()
                return redirect('taluk-list')

    context = {"menu": "menu-taluk", "form": form}
    return render(request, 'taluk/taluk_form.html', context)


def edit_taluk_entry(request, id):
    data = TalukMaster.objects.get(id=id)
    form = TalukForm(instance=data)

    if request.method == 'POST':
        form = TalukForm(request.POST, instance=data)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.taluk_name = obj.taluk_name.title()
            ward_name = obj.ward_name
            # print(ward_name)

            obj.dupcheck = f"{obj.taluk_name}{ward_name}"

            validation = TalukMaster.objects.get(dupcheck=obj.dupcheck)
            if validation and validation.id != id:
                messages.info(request, "This data already exists.")
                # obj.delete()
            else:
                # print("Not dublicate")
                obj.save()
                return redirect('taluk-list')

    context = {"menu": "menu-taluk", "form": form}
    return render(request, 'taluk/taluk_form.html', context)


def delete_taluk_entry(request, id):
    data = TalukMaster.objects.get(id=id)

    if request.method == 'POST':
        data.delete()
        return redirect('taluk-list')

    context = {"menu": "menu-taluk", "obj": data}
    return render(request, 'taluk/taluk_delete.html', context)
