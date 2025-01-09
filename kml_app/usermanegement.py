from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
# from . settings_views import user_bundle_settings
import configparser
import os
import hashlib
import requests as req
import json

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'config.ini'))

# API_STUDIO_URL = config['DEFAULT']['API_STUDIO_URL']
# API_STUDIO_URL = user_bundle_settings()



UserMasterTableName = 'asa0204_01_01'


def fetch_user_credential(request, username):
    user_data_url = f"{API_STUDIO_URL}sqlviews/api/v1/get_respone_data/"

    payload = json.dumps({
        "psk_uid": "e02e7946-e732-418d-8a88-c13105cf4696",
        "project": "public",
        "data": {
            "username": username
        }
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = req.request("POST", user_data_url, headers=headers, data=payload)
    if response.status_code != 200:
        messages.error(request, message="Sql Views Api request failed")
        return None, redirect('user_login')
    user_data = response.json()[0]


    return user_data['user_type']



def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # print(username, password)
        input_bytes = password.encode('utf-8')

        # Compute the SHA-256 hash
        hashed_value = hashlib.sha256(input_bytes).hexdigest()

        url = f"{API_STUDIO_URL}getapi/{UserMasterTableName}"

        payload = json.dumps({
            "queries": [
                {
                    "field": "username",
                    "value": username,
                    "operation": "equal"
                },
                {
                    "field": "password",
                    "value": hashed_value,
                    "operation": "equal"
                }
            ],
            "search_type": "first"
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = req.request("POST", url, headers=headers, data=payload)
        response_json = response.json()
        if response.status_code == 200:
            return redirect('list-of-values')
        else:
            messages.error(request, message="Invalid Username or Password")

    return render(request, 'login/auth_login.html')

def user_master_screen(request):
    # user_type = fetch_user_credential(request, username)
    api_url = f"{API_STUDIO_URL}getapi/{UserMasterTableName}/all"

    payload = {}
    headers = {}

    response = req.request("GET", api_url, headers=headers, data=payload)
    if response.status_code == 200:
        response_json = response.json()
    else:
        messages.error(request, message="The API is not retrieving data.")

    context = {
        "menu": "menu-usermaster",
        "response_json": response_json,

    }

    return render(request, 'usermaster/user_master_screen.html', context)

def create_user_master(request):
    api_url = f"{API_STUDIO_URL}getapi/{UserMasterTableName}/all"

    payload = {}
    headers = {}

    response = req.request("GET", api_url, headers=headers, data=payload)
    if response.status_code != 200:
        messages.error(request, message="The API is not User Master Table retrieving data.")
    response_json = response.json()

    users_names_list = [user['username'] for user in response_json]

    # api_url2 = f"{API_STUDIO_URL}getapi/{UserMasterTableName}/all"
    #
    # payload = {}
    # headers = {}
    #
    # res = req.request("GET", api_url2, headers=headers, data=payload)
    # if response.status_code != 200:
    #     messages.error(request, message=f"The API is not '{UserMasterTableName}' Table retrieving data.")
    # res_json = res.json()
    # print(res_json)
    #
    # user_role_list = []
    # for user_role in res_json:
    #     user_role_list.append({"role": user_role['user_role'], "psk_id": user_role['psk_id']})

    # print(user_role_list)

    if request.method == 'POST':
        username_data = request.POST['username']
        firstname = request.POST['firstname']
        password = request.POST['password']
        usertype = request.POST['usertype']
        email = request.POST['email']
        last_name = request.POST['last_name']
        # userrole = request.POST.getlist('userrole')
        # reporting = request.POST['reporting']
        userrole = None
        reporting = None

        input_bytes = password.encode('utf-8')
        # Compute the SHA-256 hash
        password_hashed_value = hashlib.sha256(input_bytes).hexdigest()

        crete_user_api_url = f"{API_STUDIO_URL}postapi/create/{UserMasterTableName}"

        payload = json.dumps({
            "data": {
                "username": username_data,
                "password": password_hashed_value,
                "user_type": usertype.title(),
                "first_name": firstname,
                "email": email,
                "reporting_to": reporting,
                "user_roles": userrole,
                "last_name": last_name
            }
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = req.request("POST", crete_user_api_url, headers=headers, data=payload)

        if response.status_code == 200:
            messages.success(request, message=f"The user '{username_data}' was created successfully.")
            return redirect('user_master_screen')
        else:
            error_res = response.json()
            messages.error(request, message=f"{error_res['detail']}")

    context = {
        "menu": "menu-usermaster",
        "users_names_list": users_names_list,
        # "user_role_list": user_role_list,
    }
    return render(request, 'usermaster/create_user_form.html', context)

def update_user_master(request, psk_id):
    api_url = f"{API_STUDIO_URL}getapi/{UserMasterTableName}/all"

    payload = {}
    headers = {}

    response = req.request("GET", api_url, headers=headers, data=payload)
    if response.status_code != 200:
        messages.error(request, message="The API is not User Master Table retrieving data.")
    response_json = response.json()

    users_names_list = [user['username'] for user in response_json]

    # api_url2 = f"{API_STUDIO_URL}getapi/{UserMasterTableName}/all"
    #
    # payload = {}
    # headers = {}
    #
    # res = req.request("GET", api_url2, headers=headers, data=payload)
    # if response.status_code != 200:
    #     messages.error(request, message="The API is not 'asa0201_01_01' Table retrieving data.")
    # res_json = res.json()
    # # print(res_json)
    #
    # user_role_list = []
    # for user_role in res_json:
    #     user_role_list.append({"role": user_role['user_role'], "psk_id": user_role['psk_id']})

    user_data_url = f"{API_STUDIO_URL}getapi/{UserMasterTableName}/{psk_id}"

    payload = {}
    headers = {}

    response = req.request("GET", user_data_url, headers=headers, data=payload)

    if response.status_code != 200:
        messages.error(request, message="The API is not User Master Table retrieving data.")
    user_res_json = response.json()

    # current_user_roles = user_res_json['user_roles']
    # str_without_braces = current_user_roles.strip('{}')
    # # Split the string by comma to get a list of string elements
    # str_list = str_without_braces.split(',')
    #
    # # Convert each string element to an integer
    # current_user_roles_data = [int(x) for x in str_list]
    #
    # current_role = []
    #
    # for user_data_role in res_json:
    #     for urole in current_user_roles_data:
    #         # print(urole)
    #         if urole == user_data_role['psk_id']:
    #             current_role.append(user_data_role['psk_id'])

    if request.method == 'POST':
        username_data = request.POST['username']
        firstname = request.POST['firstname']
        last_name = request.POST['last_name']
        usertype = request.POST['usertype']
        email = request.POST['email']
        # userrole = request.POST.getlist('userrole')
        # reporting = request.POST['reporting']
        userrole = None
        reporting = None

        update_user_api_url = f"{API_STUDIO_URL}updateapi/update/{UserMasterTableName}/{psk_id}"

        payload = json.dumps({
            "data": {
                "username": username_data,
                "user_type": usertype.title(),
                "first_name": firstname,
                "email": email,
                "reporting_to": reporting,
                "user_roles": userrole,
                "password": user_res_json['password'],
                "last_name": last_name
            }
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = req.request("PUT", update_user_api_url, headers=headers, data=payload)

        if response.status_code == 200:
            messages.success(request, message=f"The user '{username_data}' was updated successfully.")
            return redirect('user_master_screen')
        else:
            error_res = response.json()
            messages.error(request, message=f"{error_res['detail']}")

    context = {
        "menu": "menu-usermaster",
        # "username": username,
        # "user_type": user_type,
        "users_names_list": users_names_list,
        # "user_role_list": user_role_list,
        "obj": user_res_json,
        # "current_role": current_role

    }
    return render(request, 'usermaster/update_user_form.html', context)

def delete_user_master(request, psk_id):
    delete_user_api_url = f"{API_STUDIO_URL}deleteapi/delete/{UserMasterTableName}/{psk_id}"

    payload = {}
    headers = {}

    response = req.request("DELETE", delete_user_api_url, headers=headers, data=payload)

    if response.status_code == 200:
        messages.success(request, message=f"The user  was deleted successfully.")
        return redirect('user_master_screen')
    else:
        error_res = response.json()
        messages.error(request, message=f"{error_res['detail']}")

def user_menus(request):

    return render(request, 'login/user_menus.html')