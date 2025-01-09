from django.db.models import Q
from django.shortcuts import render, redirect
from .models import ListType
from .forms import ListTypeForm
from django.contrib import messages
from django.db import IntegrityError


def get_all_type(request):
    obj = ListType.objects.all().order_by('list_type')
    context = {"menu": "menu-type", "obj": obj}
    return render(request, 'list_type/list_type_data.html', context)


def new_type_entry(request):
    form = ListTypeForm()
    if request.method == 'POST':
        form = ListTypeForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.list_type = obj.list_type.title()
            try:
                obj.save()
                return redirect('list-type')
            except Exception as e:
                messages.error(request, message=f"{e}")
            except IntegrityError:
                messages.info(request, 'This data already exists.')

        else:
            messages.info(request, 'This data already exists.')
    context = {"menu": "menu-type", "form": form, "head": "New List Type"}
    return render(request, 'list_type/list_type_form.html', context)


# def edit_list_type(request, id):
#     data = ListType.objects.get(id=id)
#     form = ListTypeForm(instance=data)
#
#     if request.method == 'POST':
#         form = ListTypeForm(request.POST, instance=data)
#         if form.is_valid():
#             obj = form.save(commit=False)
#             obj.list_type = obj.list_type.title()
#             try:
#                 obj.save()
#                 return redirect('list-type')
#             except IntegrityError:
#                 messages.info(request, 'This data already exists.')
#         else:
#             messages.info(request, 'This data already exists.')
#
#     context = {"menu": "menu-type", "form": form, "head": "Edit List Type"}
#     return render(request, 'list_type/list_type_form.html', context)


# def delete_list_type(request, id):
#     data = ListType.objects.get(id=id)
#
#     if request.method == 'POST':
#         data.delete()
#         return redirect('list-type')
#
#     context = {"menu": "menu-type", "obj": data}
#     return render(request, 'list_type/list_type_delete.html', context)


def li_search_values(request):
    search_query = request.GET.get('search', '')
    # print(search_query)
    search_filter = (
           Q(list_type__icontains=search_query)
    )
    # print(search_filter)
    obj = ListType.objects.filter(search_filter).order_by('list_type')
    # print(obj)

    context = {"menu": "menu-type", "obj": obj, "search_query": search_query}
    return render(request, 'list_type/list_type_data.html', context)

