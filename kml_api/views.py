from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes

from kml_app import list_of_values
from .serializers import *
import zipfile
import pandas as pd
from kml_app.models import *



@api_view(http_method_names=['GET'])
def boundary_pillar_photos(request: Request, unique_id):
    scheme = f"{request.scheme}s"
    # print(scheme)
    host = request.get_host()
    server_url = f"{scheme}://{host}"

    try:

        if not unique_id:
            raise ValueError("Unique ID is required.")

        # Fetch the parent cadastral entry
        parent_obj = CadastralEntry.objects.get(unique_id=unique_id)

        # Fetch the sub cadastral entry associated with the parent
        obj = SubCadastralEntry.objects.filter(cadastral_entry=parent_obj.id)

        # Serialize the boundary pillar photos
        serializer = BoundaryPillarPhotoSerializer(instance=obj, many=True)

        # print(serializer.data)
        response = {"boundary_pillar_photos": serializer.data , "url": server_url}
        return Response(data=response, status=status.HTTP_200_OK)
    except CadastralEntry.DoesNotExist:
        return Response({"error": "Cadastral entry not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['GET'])
def list_types(request: Request):
    obj = ListType.objects.all()

    serializer = ListTypeSerializer(instance=obj, many=True)

    response = {"ListType": serializer.data}
    return Response(data=response, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
def list_of_values_list(request: Request):
    obj = ListOFValues.objects.all()
    serializer = ListOfValuesSerializer(instance=obj, many=True)
    # print(serializer.data)
    response = {"ListOFValues": serializer.data}
    return Response(data=response, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
def cadastral_master_kml(request: Request, river_name: str):
    river_name_id = get_object_or_404(ListOFValues, list_of_values=river_name)
    obj = CadastralMasterKMLTable.objects.get(list_type__name="River Name",river_name=river_name_id)
    # print(obj)

    file_path = obj.kml_file.path
    # print(file_path)

    if file_path.lower().endswith('.kml'):
        with open(file_path, 'r') as kml_file:
            kml_data = kml_file.read()

        response = HttpResponse(kml_data, content_type='application/vnd.google-earth.kml+xml')
        response['Content-Disposition'] = f'attachment; filename="{id}.kml"'
        return response

    elif file_path.lower().endswith('.kmz'):
        with zipfile.ZipFile(file_path, 'r') as kmz_zip:
            # Assuming there is only one KML file in the KMZ
            kml_filename = [f for f in kmz_zip.namelist() if f.lower().endswith('.kml')][0]
            kml_data = kmz_zip.read(kml_filename).decode('utf-8')

        response = HttpResponse(kml_data, content_type='application/vnd.google-earth.kml+xml')
        response['Content-Disposition'] = f'attachment; filename="{kml_filename}"'
        return response

    else:
        return Response({"error": "Invalid file type. Supported file types are KML and KMZ."}, status=400)


@api_view(http_method_names=['GET'])
def boundary_pillar_kml(request: Request, river_name: str):
    river_name_id = get_object_or_404(ListOFValues, list_of_values=river_name)
    obj = BoundaryKMLTable.objects.get(river_name=river_name_id)
    # print(obj)

    file_path = obj.kml_file.path
    # print(file_path)

    if file_path.lower().endswith('.kml'):
        with open(file_path, 'r') as kml_file:
            kml_data = kml_file.read()

        response = HttpResponse(kml_data, content_type='application/vnd.google-earth.kml+xml')
        response['Content-Disposition'] = f'attachment; filename="{id}.kml"'
        return response

    elif file_path.lower().endswith('.kmz'):
        with zipfile.ZipFile(file_path, 'r') as kmz_zip:
            # Assuming there is only one KML file in the KMZ
            kml_filename = [f for f in kmz_zip.namelist() if f.lower().endswith('.kml')][0]
            kml_data = kmz_zip.read(kml_filename).decode('utf-8')

        response = HttpResponse(kml_data, content_type='application/vnd.google-earth.kml+xml')
        response['Content-Disposition'] = f'attachment; filename="{kml_filename}"'
        return response

    else:
        return Response({"error": "Invalid file type. Supported file types are KML and KMZ."}, status=400)


@api_view(http_method_names=['GET'])
def enchrochment_kml(request: Request, river_name: str):
    river_name_id = get_object_or_404(ListOFValues, list_of_values=river_name)
    obj = EnchrochKMLTable.objects.get(river_name=river_name_id)
    # print(obj)

    file_path = obj.kml_file.path
    # print(file_path)

    if file_path.lower().endswith('.kml'):
        with open(file_path, 'r') as kml_file:
            kml_data = kml_file.read()

        response = HttpResponse(kml_data, content_type='application/vnd.google-earth.kml+xml')
        response['Content-Disposition'] = f'attachment; filename="{id}.kml"'
        return response

    elif file_path.lower().endswith('.kmz'):
        with zipfile.ZipFile(file_path, 'r') as kmz_zip:
            # Assuming there is only one KML file in the KMZ
            kml_filename = [f for f in kmz_zip.namelist() if f.lower().endswith('.kml')][0]
            kml_data = kmz_zip.read(kml_filename).decode('utf-8')

        response = HttpResponse(kml_data, content_type='application/vnd.google-earth.kml+xml')
        response['Content-Disposition'] = f'attachment; filename="{kml_filename}"'
        return response

    else:
        return Response({"error": "Invalid file type. Supported file types are KML and KMZ."}, status=400)


@api_view(http_method_names=['GET'])
def intrusion_kml(request: Request, river_name: str):
    river_name_id = get_object_or_404(ListOFValues, list_of_values=river_name)
    obj = IntrusionKMLTable.objects.get(river_name=river_name_id)
    # print(obj)

    file_path = obj.kml_file.path
    # print(file_path)

    if file_path.lower().endswith('.kml'):
        with open(file_path, 'r') as kml_file:
            kml_data = kml_file.read()

        response = HttpResponse(kml_data, content_type='application/vnd.google-earth.kml+xml')
        response['Content-Disposition'] = f'attachment; filename="{id}.kml"'
        return response

    elif file_path.lower().endswith('.kmz'):
        with zipfile.ZipFile(file_path, 'r') as kmz_zip:
            # Assuming there is only one KML file in the KMZ
            kml_filename = [f for f in kmz_zip.namelist() if f.lower().endswith('.kml')][0]
            kml_data = kmz_zip.read(kml_filename).decode('utf-8')

        response = HttpResponse(kml_data, content_type='application/vnd.google-earth.kml+xml')
        response['Content-Disposition'] = f'attachment; filename="{kml_filename}"'
        return response

    else:
        return Response({"error": "Invalid file type. Supported file types are KML and KMZ."}, status=400)

@api_view(http_method_names=['GET'])
def street_lists(request: Request):
    obj = StreetMaster.objects.all()
    serializer = StreetSerializer(instance=obj, many=True)
    response = {"Street": serializer.data}

    return Response(data=response, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
def cadastral_line_lists(request: Request):
    obj = CadastralMaster.objects.all()
    serializer = CadastralMasterSerializer(instance=obj, many=True)
    response = {"CadastralLine": serializer.data}

    return Response(data=response, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
def boundary_pillar_lists(request: Request):
    obj = CadastralEntry.objects.all()
    print(obj)
    serializer = CadastralEntrySerializerForm(instance=obj, many=True)
    response = {"BoundaryPillar": serializer.data}

    return Response(data=response, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
def enchrochments_lists(request: Request):
    obj = CadastralDeviation.objects.all()
    serializer = CadastralDeviationSerializerForm(instance=obj, many=True)
    response = {"Enchrochments": serializer.data}

    return Response(data=response, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
def intrusion_lists(request: Request):
    obj = IntrusionMaster.objects.all()
    serializer = IntrusionMasterSerializer(instance=obj, many=True)
    response = {"Intrusion": serializer.data}

    return Response(data=response, status=status.HTTP_200_OK)


@api_view(['POST'])
# @parser_classes([FileUploadParser])
def list_type_excel(request):
    if request.method == 'POST':

        obj_count = 0
        existing_obj_count = 0

        uploaded_file = request.data.get('excel_file')
        if not uploaded_file or not uploaded_file.name.endswith('.xls') and not uploaded_file.name.endswith('.xlsx'):
            response = {"error": "Please upload a valid Excel file."}
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        serializer = ListTypeExcelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        obj = ListofValuesExcelTable.objects.last()
        uploaded_file_path = obj.excel_file.path

        try:
            # Assuming you are using pandas to read the Excel file
            df = pd.read_excel(uploaded_file_path)
            # print(df)

            # Normalize column names to lowercase and remove spaces
            df.columns = df.columns.str.lower().str.replace(' ', '_')

            total_rows = len(df)
            total_column = len(df.columns)

            # Assuming your DataFrame has columns like 'list_type' and 'list_of_values'
            for index, row in df.iterrows():
                list_type_id = ListType.objects.get(list_type=str(row['list_type']).strip()).id
                list_of_values = row['list_of_values']
                active = row['active']
                dupcheck = f"{row['list_type'].strip()}{list_of_values.strip()}{active}"

                # Check if a record with the same dupcheck value exists
                existing_record = ListOFValues.objects.filter(dupcheck=dupcheck).first()

                if existing_record:
                    # Update the existing record or handle it as needed
                    existing_obj_count += 1
                    existing_record.list_type_id = list_type_id
                    existing_record.list_of_values = list_of_values
                    existing_record.active = active
                    existing_record.save()
                else:
                    obj_count += 1
                    ListOFValues.objects.create(
                        list_type_id=list_type_id,
                        list_of_values=str(list_of_values).strip(),
                        active=active,
                        dupcheck=dupcheck
                    )
            # print("Total objects created:", obj_count)
            # print("Existing Record  created:", existing_obj_count)

            response = {
                "Status": "Imported Successfully",
                "total_rows": total_rows,
                "total_column": total_column,
                "create_obj_count": obj_count,
                "existing_obj_count": existing_obj_count
            }
            return Response(data=response, status=status.HTTP_201_CREATED)

        except KeyError as e:
            error_message = f"Column '{e.args[0]}' not found in the Excel file."
            response = {"error": error_message}
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def street_excel_import(request: Request):
    if request.method == 'POST':
        obj_count = 0
        existing_obj_count = 0

        uploaded_file = request.data.get('excel_file')
        if not uploaded_file or not uploaded_file.name.endswith('.xls') and not uploaded_file.name.endswith('.xlsx'):
            response = {"error": "Please upload a valid Excel file."}
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        serializer = StreetExcelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        obj = StreetExcelTable.objects.last()
        uploaded_file_path = obj.excel_file.path

        try:
            # Assuming you are using pandas to read the Excel file
            df = pd.read_excel(uploaded_file_path)

            # Normalize column names to lowercase and remove spaces
            df.columns = df.columns.str.lower().str.replace(' ', '_')

            total_rows = len(df)

            # Assuming your DataFrame has columns like 'list_type' and 'list_of_values'
            for index, row in df.iterrows():
                try:

                    river_name = row['river_name']
                    block_name = row['block_name']
                    sub_basin = row['sub_basin']
                    district_name = row['district_name']
                    town_name = row['town_name']
                    taluk_name = row['taluk_name']

                    street_name = row['street_name']
                    survey_no = row['survey_no']
                    classification = row['classification']

                    sub_classification = row['sub_classification']

                    lattitude = row['easting']
                    langitutte = row['northing']

                    query_list = [
                        'river_name', 'block_name', 'sub_basin', 'district_name', 'town_name',
                        'taluk_name', 'classification', 'sub_classification'
                    ]
                    # print(taluk_name)
                    for query in query_list:
                        try:
                            if query == "town_name":
                                query_obj = ListOFValues.objects.get(list_of_values=str(row[query]).strip(),
                                                                     list_type__list_type="Town")
                            elif query == "taluk_name":
                                query_obj = ListOFValues.objects.get(list_of_values=str(row[query]).strip(),
                                                                     list_type__list_type="Taluk")

                            else:
                                query_obj = ListOFValues.objects.get(list_of_values=str(row[query]).strip())
                        except ListOFValues.DoesNotExist:
                            response = {"error": f"Not found {query} in ListOFValues: {row[query]}"}
                            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
                        except ListOFValues.MultipleObjectsReturned:
                            response = {"error": f"Multiple ListOFValues objects found with {query}: {row[query]}"}
                            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                    dupcheck = f"{river_name}{block_name}{sub_basin}{district_name}{town_name}{taluk_name}"
                    # child_dupcheck = f"{street_name}{survey_no}{classification}{sub_classification}{lattitude}{langitutte}"
                    child_dupcheck = f"{lattitude}{langitutte}"
                    # print(dupcheck)

                    existing_record = StreetMaster.objects.filter(dupcheck=dupcheck).first()

                    if existing_record:
                        id = existing_record.id
                        # print(id)

                    else:
                        # Create a ListOFValues instance and save it
                        # print("New Data Create")

                        river_name_id = ListOFValues.objects.get(list_of_values=str(row['river_name']).strip()).id
                        block_name_id = ListOFValues.objects.get(list_of_values=str(row['block_name']).strip()).id
                        sub_basin_id = ListOFValues.objects.get(list_of_values=str(row['sub_basin']).strip()).id
                        district_name_id = ListOFValues.objects.get(list_of_values=str(row['district_name']).strip()).id
                        town_name_id = ListOFValues.objects.get(list_of_values=str(row['town_name']).strip(),
                                                                list_type__list_type="Town").id
                        taluk_name_id = ListOFValues.objects.get(list_of_values=str(row['taluk_name']).strip(),
                                                                 list_type__list_type="Taluk").id

                        StreetMaster.objects.create(
                            river_name_id=river_name_id,
                            block_name_id=block_name_id,
                            sub_basin_id=sub_basin_id,
                            district_name_id=district_name_id,
                            town_name_id=town_name_id,
                            taluk_name_id=taluk_name_id,
                            dupcheck=dupcheck
                        )

                        id = StreetMaster.objects.last().id

                    child_existing_record = SurveyMaster.objects.filter(dupcheck=child_dupcheck).first()
                    # print(child_existing_record)

                    if child_existing_record:
                        sub_classification_id = ListOFValues.objects.get(
                            list_of_values=str(row['sub_classification']).strip()).id
                        classification_id = ListOFValues.objects.get(
                            list_of_values=str(row['classification']).strip()).id

                        existing_obj_count += 1
                        # child_id = child_existing_record
                        # print(type(child_id))
                        # print(child_id.id)
                        # obj = SurveyMaster.objects.get(id=child_id)
                        child_existing_record.street_name = street_name
                        child_existing_record.survey_no = survey_no
                        child_existing_record.classification_id = classification_id
                        child_existing_record.sub_classification_id = sub_classification_id
                        child_existing_record.lattitude = langitutte
                        child_existing_record.langitutte = lattitude
                        child_existing_record.street_master_id = id
                        child_existing_record.save()
                        # print("block_name", block_name)
                        # print("survey_no", survey_no, child_existing_record.survey_no, child_existing_record.id)

                        pass
                    else:

                        sub_classification_id = ListOFValues.objects.get(
                            list_of_values=str(row['sub_classification']).strip()).id
                        classification_id = ListOFValues.objects.get(
                            list_of_values=str(row['classification']).strip()).id

                        obj_count += 1
                        try:
                            SurveyMaster.objects.create(
                                street_name=street_name,
                                survey_no=survey_no,
                                classification_id=classification_id,
                                sub_classification_id=sub_classification_id,
                                lattitude=langitutte,
                                langitutte=lattitude,
                                street_master_id=id,
                                dupcheck=child_dupcheck
                            )
                        except IntegrityError as e:
                            # Handle the IntegrityError here
                            # For example, you can print an error message
                            # print("IntegrityError:", e)
                            if "kml_app_surveymaster.langitutte" in str(e):
                                response = {"error": "Duplicate value found in: NORTHING"}
                            else:
                                response = {"error": "Duplicate value found in: EASTING"}

                            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                except ListOFValues.DoesNotExist as e:
                    error_row = index + 2
                    # print(error_row)
                    error_message = f"Row: {error_row}, Wrong Data: '{e.args[0]}'"
                    response = {"error": error_message}
                    return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

            response = {
                "Status": "Imported Successfully",
                "total_rows": total_rows,
                "create_obj_count": obj_count,
                "existing_obj_count": existing_obj_count
            }

            # response = {"Status": "Imported Successfully"}
            return Response(data=response, status=status.HTTP_201_CREATED)

        except KeyError as e:
            error_message = f"Column '{e.args[0]}' not found in the Excel file."
            response = {"error": error_message}
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


def normalize_value(value):
    if value is None:
        return None
    elif isinstance(value, float):
        return str(int(value)) if value.is_integer() else str(value)
    else:
        return str(value)


@api_view(['POST'])
def CM_excel_import(request: Request):
    # print("CM_excel_import")
    if request.method == 'POST':

        obj_count = 0
        existing_obj_count = 0

        uploaded_file = request.data.get('excel_file')
        if not uploaded_file or not uploaded_file.name.endswith('.xls') and not uploaded_file.name.endswith('.xlsx'):
            response = {"error": "Please upload a valid Excel file."}
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        serializer = CadastralMasterExcelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        obj = CadastralMasterExcelTable.objects.last()
        uploaded_file_path = obj.excel_file.path

        try:
            # Assuming you are using pandas to read the Excel file
            df = pd.read_excel(uploaded_file_path)
            # print(df)

            # Normalize column names to lowercase and remove spaces
            df.columns = df.columns.str.lower().str.replace(' ', '_')
            df = df.fillna('NA')
            total_rows = len(df)
            # Assuming your DataFrame has columns like 'list_type' and 'list_of_values'
            for index, row in df.iterrows():
                try:

                    # river_name_id = ListOFValues.objects.get(list_of_values=row['river_name']).id
                    # print(row)
                    unique_id = row['unique_id']
                    river_name = row['river_name']
                    block_name = row['block_name']
                    sub_basin = row['sub_basin']
                    survey_no = row['survey_no']
                    district_name = row['district_name']
                    town_name = row['town_name']
                    taluk_name = row['taluk_name']
                    zone = row['zone']
                    ward = row['ward']
                    town_survey_no = row['town_survey_no']
                    village_name = row['village_name']
                    sub_division_no = row['sub_div_no']

                    query_list = ['river_name', 'block_name', 'sub_basin', 'district_name', 'town_name', 'taluk_name']
                    # print(taluk_name)
                    for query in query_list:
                        try:
                            if query == "town_name":
                                query_obj = ListOFValues.objects.get(list_of_values=str(row[query]).strip(),
                                                                     list_type__list_type="Town")
                            elif query == "taluk_name":
                                query_obj = ListOFValues.objects.get(list_of_values=str(row[query]).strip(),
                                                                     list_type__list_type="Taluk")
                            elif query == "block_name":
                                query_obj = ListOFValues.objects.get(list_of_values=str(row[query]).strip(),
                                                                     list_type__list_type="Block")
                            else:
                                query_obj = ListOFValues.objects.get(list_of_values=str(row[query]).strip())

                        except ListOFValues.DoesNotExist:
                            response = {"error": f"Error Line : {index + 2} Not found {query} in ListOFValues: {row[query]}"}
                            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
                        except ListOFValues.MultipleObjectsReturned:
                            response = {"error": f"Multiple ListOFValues objects found with {query}: {row[query]}"}
                            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                    latitude = row['easting']

                    longitude = row['northing']

                    dupcheck = f"{unique_id}"
                    child_dupcheck = f"{latitude}{longitude}"
                    # print(dupcheck)

                    existing_record = CadastralMaster.objects.filter(unique_id=unique_id).first()

                    if existing_record:
                        # Update the existing record or handle it as needed
                        print("Already Data Exits")



                        id = existing_record.id
                        river_name_id = ListOFValues.objects.get(list_of_values=str(row['river_name']).strip()).id

                        existing_record.unique_id = unique_id
                        existing_record.river_name_id = river_name_id
                        existing_record.block = block_name
                        existing_record.sub_bassin = sub_basin
                        existing_record.survey_no = survey_no
                        existing_record.district = district_name
                        existing_record.town = town_name
                        existing_record.taluk = taluk_name

                        existing_record.zone = normalize_value(zone)
                        existing_record.ward = normalize_value(ward)
                        existing_record.town_survey_no = normalize_value(town_survey_no)
                        existing_record.village_name = normalize_value(village_name)
                        existing_record.sub_division_no = normalize_value(sub_division_no)


                        existing_record.save()


                    else:
                        # Create a ListOFValues instance and save it
                        # print("New Data Create")
                        river_name_id = ListOFValues.objects.get(list_of_values=str(row['river_name']).strip()).id

                        CadastralMaster.objects.create(
                            unique_id=unique_id,
                            river_name_id=river_name_id,
                            block=block_name,
                            sub_bassin=sub_basin,
                            survey_no=survey_no,
                            district=district_name,
                            town=town_name,
                            taluk=taluk_name,
                            dupcheck=dupcheck,
                            zone=zone,
                            ward = ward,
                            town_survey_no = town_survey_no,
                            village_name = village_name,
                            sub_division_no = sub_division_no,
                        )

                        id = CadastralMaster.objects.last().id

                    child_existing_record = SubCadastralLine.objects.filter(dupcheck=child_dupcheck)

                    if child_existing_record:
                        # print("child_existing_record")
                        existing_obj_count += 1
                        pass
                    else:
                        obj_count += 1
                        SubCadastralLine.objects.create(
                            lat=latitude,
                            long=longitude,
                            cadastral_id=id,
                            dupcheck=child_dupcheck

                        )

                # except ListOFValues.DoesNotExist as e:
                #     # Handle the exception and return a custom response
                #     error_message = f"Row: {df.shape[0]}, Wrong Data: '{e.args[0]}'"
                #     response = {"error": error_message}
                #     return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    error_message = f"Error in row {index + 2}, column {e.args[0]}"
                    response = {"error": error_message}
                    return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

            response = {
                "Status": "Imported Successfully",
                "total_rows": total_rows,
                "create_obj_count": obj_count,
                "existing_obj_count": existing_obj_count
            }
            return Response(data=response, status=status.HTTP_201_CREATED)

        except KeyError as e:
            # print(df.iterrows)
            error_message = f"Error Line {df.shape[0]} Column '{e.args[0]}' not found in the Excel file."
            response = {"error": error_message}
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def boundaryPillar_excel_import(request: Request):
    if request.method == 'POST':

        obj_count = 0
        existing_obj_count = 0

        uploaded_file = request.data.get('excel_file')
        if not uploaded_file or not uploaded_file.name.endswith('.xls') and not uploaded_file.name.endswith('.xlsx'):
            response = {"error": "Please upload a valid Excel file."}
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        serializer = CadastralEntrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        obj = CadastralEntryExcelTable.objects.last()
        uploaded_file_path = obj.excel_file.path
        # response = {"Status": "Imported Successfully"}
        # return Response(data=response, status=status.HTTP_201_CREATED)

        try:
            # Assuming you are using pandas to read the Excel file
            df = pd.read_excel(uploaded_file_path)
            # print(df)

            # Normalize column names to lowercase and remove spaces
            df.columns = df.columns.str.lower().str.replace(' ', '_')
            df = df.fillna('NA')

            total_rows = len(df)
            # Assuming your DataFrame has columns like 'list_type' and 'list_of_values'

            for index, row in df.iterrows():
                river_name = row['river_name']
                river_bank = row['river_bank']

                unique_id = row['unique_id']
                sub_bassin = row['sub_basin']
                town = row['town_name']
                taluk = row['taluk_name']
                district = row['district_name']
                block = row['block_name']
                tsno_sdno = str(row['survey_no']).strip()
                classify = row['classification']
                sub_classify = row['sub_classification']
                latitude = row['easting']
                longitude = row['northing']
                elevation = row['elevation']
                type_of_pillar = row['type_of_pillar']
                street = row['street_name']
                remarks = row['remarks']
                zone = row['zone']
                ward = row['ward']
                town_survey_no = row['town_survey_no']
                village_name = row['village_name']
                sub_division_no = row['sub_div_no']

                query_list = [
                    'river_name', 'river_bank', 'block_name',
                    'sub_basin', 'district_name', 'town_name', 'taluk_name',
                    'classification', 'sub_classification', 'type_of_pillar'

                ]
                # print(taluk_name)
                for query in query_list:
                    try:
                        if query == "town_name":
                            query_obj = ListOFValues.objects.get(list_of_values=str(row[query]).strip(),
                                                                 list_type__list_type="Town")
                        elif query == "taluk_name":
                            query_obj = ListOFValues.objects.get(list_of_values=str(row[query]).strip(),
                                                                 list_type__list_type="Taluk")

                        elif query == "block_name":
                            query_obj = ListOFValues.objects.get(list_of_values=str(row[query]).strip(),
                                                                 list_type__list_type="Block")
                        else:
                            query_obj = ListOFValues.objects.get(list_of_values=str(row[query]).strip())

                    except ListOFValues.DoesNotExist:
                        response = {"error": f" Error Line {index+2} Not found in {query} ListOFValues : {row[query]}"}
                        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
                    except ListOFValues.MultipleObjectsReturned:
                        response = {"error": f" Error Line {index+2} Multiple ListOFValues objects found with {query}: {row[query]}"}
                        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                street_list = ['street_name']

                for street_obj in street_list:
                    try:
                        query_obj = SurveyMaster.objects.filter(street_name=str(row[street_obj]).strip())
                        if not query_obj:
                            response = {"error": f" Error Line : {index + 2} No Street object found with {street_obj}: {row[street_obj]}"}
                            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                    except SurveyMaster.DoesNotExist:
                        response = {"error": f"Error Line : {index + 2} No Street object found with {street_obj}: {row[street_obj]}"}
                        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
                    except SurveyMaster.MultipleObjectsReturned:
                        response = {"error": f"Multiple Street objects found with {street_obj}: {row[street_obj]}"}
                        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                # survey_no = 'survey_no'
                # try:
                #     query_obj = SurveyMaster.objects.filter(survey_no=str(row[survey_no]).strip())
                #     if not query_obj:
                #         response = {"error": f"Error Line : {index + 2} No Street object found with {survey_no}: {row[survey_no]}"}
                #         return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
                # except SurveyMaster.DoesNotExist:
                #     response = {"error": f"Error Line : {index + 2} No Street object found with {survey_no}: {row[survey_no]}"}
                #     return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
                # except SurveyMaster.MultipleObjectsReturned:
                #     response = {"error": f"Multiple Street objects found with {survey_no}: {row[survey_no]}"}
                #     return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                easting = 'easting'

                try:
                    query_obj = SurveyMaster.objects.filter(langitutte=str(row[easting]).strip())
                    if not query_obj:
                        response = {"error": f"No Street object found with {easting}: {row[easting]}"}
                        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
                except SurveyMaster.DoesNotExist:
                    response = {"error": f"No Street object found with {easting}: {row[easting]}"}
                    return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
                # except SurveyMaster.MultipleObjectsReturned:
                #     response = {"error": f"Multiple Street objects found with {easting}: {row[easting]}"}
                #     return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                northing = 'northing'
                try:
                    query_obj = SurveyMaster.objects.get(lattitude=str(row[northing]).strip())
                    if not query_obj:
                        response = {"error": f"No Street object found with {northing}: {row[northing]}"}
                        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
                except SurveyMaster.DoesNotExist:
                    response = {"error": f"No Street object found with {northing}: {row[northing]}"}
                    return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
                # except SurveyMaster.MultipleObjectsReturned:
                #     response = {"error": f"Multiple Street objects found with {northing}: {row[northing]}"}
                #     return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                dupcheck = f"{unique_id}"

                # Check if a record with the same dupcheck value exists
                # existing_record = CadastralEntry.objects.filter(dupcheck=dupcheck).first()
                existing_record = CadastralEntry.objects.filter(unique_id=unique_id).first()

                # latitude = CadastralEntry.objects.filter(latitude=latitude).first()

                if existing_record:

                    existing_obj_count += 1
                    river_name_id = ListOFValues.objects.get(list_of_values=str(row['river_name']).strip()).id
                    river_bank_id = ListOFValues.objects.get(list_of_values=str(row['river_bank']).strip()).id
                    existing_record.river_name_id = river_name_id
                    existing_record.river_bank_id = river_bank_id
                    existing_record.unique_id = unique_id
                    existing_record.sub_bassin = sub_bassin
                    existing_record.town = town
                    existing_record.taluk = taluk
                    existing_record.district = district
                    existing_record.block = block
                    existing_record.tsno_sdno = tsno_sdno
                    existing_record.classify = classify
                    existing_record.sub_classify = sub_classify
                    existing_record.latitude = latitude
                    existing_record.longitude = longitude
                    existing_record.elevation = elevation
                    existing_record.type_of_pillar = type_of_pillar
                    existing_record.street = street
                    existing_record.remarks = remarks

                    existing_record.zone = normalize_value(zone)
                    existing_record.ward = normalize_value(ward)
                    existing_record.town_survey_no = normalize_value(town_survey_no)
                    existing_record.village_name = normalize_value(village_name)
                    existing_record.sub_division_no = normalize_value(sub_division_no)

                    existing_record.save()
                    pass

                else:
                    # print("else working")
                    obj_count += 1
                    # Create a ListOFValues instance and save it
                    river_name_id = ListOFValues.objects.get(list_of_values=str(row['river_name']).strip()).id
                    river_bank_id = ListOFValues.objects.get(list_of_values=str(row['river_bank']).strip()).id

                    try:
                        CadastralEntry.objects.create(
                            river_name_id=river_name_id,
                            river_bank_id=river_bank_id,
                            unique_id=unique_id,
                            sub_bassin=sub_bassin,
                            town=town,
                            taluk=taluk,
                            district=district,
                            block=block,
                            tsno_sdno=tsno_sdno,
                            classify=classify,
                            sub_classify=sub_classify,
                            latitude=latitude,
                            longitude=longitude,
                            elevation=elevation,
                            type_of_pillar=type_of_pillar,
                            street=street,
                            remarks=remarks,
                            dupcheck=dupcheck,
                            zone=zone,
                            ward=ward,
                            town_survey_no=town_survey_no,
                            village_name=village_name,
                            sub_division_no=sub_division_no,
                        )
                    except IntegrityError as e:
                        detail_message = str(e).split("DETAIL:")[1].strip()
                        response = {"error": f"""Duplicate value 
                         DETAIL: {detail_message}
                         """}
                        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

            response = {
                "Status": "Imported Successfully",
                "total_rows": total_rows,
                "create_obj_count": obj_count,
                "existing_obj_count": existing_obj_count
            }
            return Response(data=response, status=status.HTTP_201_CREATED)

        except KeyError as e:
            error_message = f"Column '{e.args[0]}' not found in the Excel file."
            # print(error_message)
            response = {"error": error_message}
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def CD_excel_import(request: Request):
    if request.method == 'POST':

        obj_count1 = 0
        obj_count2 = 0
        obj_count3 = 0
        existing_obj_count = 0

        uploaded_file = request.data.get('excel_file')
        if not uploaded_file or not uploaded_file.name.endswith('.xls') and not uploaded_file.name.endswith('.xlsx'):
            response = {"error": "Please upload a valid Excel file."}
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        serializer = CadastralDeviationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        obj = CadastralDeviationExcelTable.objects.last()
        uploaded_file_path = obj.excel_file.path

        try:
            # Assuming you are using pandas to read the Excel file
            df = pd.read_excel(uploaded_file_path)
            # print(df)

            # Normalize column names to lowercase and remove spaces
            df.columns = df.columns.str.lower().str.replace(' ', '_')
            df = df.fillna('NA')

            total_rows = len(df)

            # Assuming your DataFrame has columns like 'list_type' and 'list_of_values'
            for index, row in df.iterrows():
                try:
                    unique_id = row['unique_id']
                    river_name = row['river_name']
                    block_name = row['block_name']
                    sub_basin = row['sub_basin']
                    district_name = row['district_name']
                    town_name = row['town_name']
                    taluk_name = row['taluk_name']
                    street_name = row['street_name']
                    ts_so_no = row['survey_no']
                    classification = row['classification']
                    sub_classification = row['sub_classification']
                    # asset_type = row['asset_type']
                    hectare = row['hectare']
                    area = row['ares']
                    sqm = row['sqm']
                    # buildings = row['buildings']
                    # no_of_buildings = row['no_of_buildings']
                    # no_of_floors = row['no_of_floors']
                    # usage_of_build = row['usage_of_build']
                    # occupier_name = row['occupier_name']
                    enchorochment = row['enchrochment']
                    remarks = row['remarks']

                    enchrochment_type = str(row['enchrochment_type']).strip()
                    # print(enchrochment_type)

                    point_id = row['point_id']

                    latitude = row['easting']
                    longitude = row['northing']
                    elevation = row['elevation']
                    # point_type = row['point_type']

                    zone = row['zone']
                    ward = row['ward']
                    town_survey_no = row['town_survey_no']
                    village_name = row['village_name']
                    sub_division_no = row['sub_div_no']

                    query_list = [
                        'river_name', 'block_name',
                        'sub_basin', 'district_name', 'town_name', 'taluk_name',
                        'classification', 'sub_classification'

                    ]
                    # print(taluk_name)
                    for query in query_list:
                        try:
                            if query == "town_name":
                                query_obj = ListOFValues.objects.get(list_of_values=str(row[query]).strip(),
                                                                     list_type__list_type="Town")
                            elif query == "taluk_name":
                                query_obj = ListOFValues.objects.get(list_of_values=str(row[query]).strip(),
                                                                     list_type__list_type="Taluk")
                            elif query == "block_name":
                                query_obj = ListOFValues.objects.get(list_of_values=str(row[query]).strip(),
                                                                     list_type__list_type="Block")
                            else:
                                query_obj = ListOFValues.objects.get(list_of_values=str(row[query]).strip())

                        except ListOFValues.DoesNotExist:
                            response = {"error": f""" Error Line : "{index + 2}"
                            Not found {query} in ListOFValues: {row[query]}"""}
                            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
                        except ListOFValues.MultipleObjectsReturned:
                            response = {"error": f"""  Error Line : "{index + 2}" 
                            Multiple ListOFValues objects found with {query}: {row[query]}"""}
                            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                    street_list = ['street_name']

                    for street_obj in street_list:
                        try:
                            query_obj = SurveyMaster.objects.filter(street_name=str(row[street_obj]).strip())
                            if not query_obj:
                                response = {"error": f""" Error Line : "{index + 2}"
                                No Street object found with {street_obj}: {row[street_obj]}"""}
                                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
                        except SurveyMaster.DoesNotExist:
                            response = {"error": f""" Error Line : "{index + 2}"
                            No Street object found with {street_obj}: {row[street_obj]}"""}
                            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
                        # except SurveyMaster.MultipleObjectsReturned:
                        #     response = {"error": f"Multiple Street objects found with {street_obj}: {row[street_obj]}"}
                        #     return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                    # survey_no = 'survey_no'
                    # try:
                    #     query_obj = SurveyMaster.objects.filter(survey_no=str(row[survey_no]).strip())
                    #     if not query_obj:
                    #         response = {"error": f""" Error Line : "{index + 2}"
                    #         No Street object found with {survey_no}: {row[survey_no]}"""}
                    #         return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
                    # except SurveyMaster.DoesNotExist:
                    #     response = {"error": f""" Error Line : "{index + 2}"
                    #     No Street object found with {survey_no}: {row[survey_no]}"""}
                    #     return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
                    # except SurveyMaster.MultipleObjectsReturned:
                    #     response = {"error": f"Multiple Street objects found with {survey_no}: {row[survey_no]}"}
                    #     return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                    # print(point_type_id)

                    dupcheck = f"{unique_id}"
                    # print(dupcheck)
                    child_dupcheck = f"{latitude}{longitude}"

                    existing_record = CadastralDeviation.objects.filter(unique_id=unique_id).first()

                    if existing_record:
                        id = existing_record.id
                        # print(id)
                        river_name_id = ListOFValues.objects.get(list_of_values=row['river_name']).id

                        existing_record.unique_id = unique_id
                        existing_record.cadastral_master_id_id = river_name_id
                        existing_record.block = block_name
                        existing_record.ward = sub_basin
                        existing_record.district = district_name
                        existing_record.town = town_name
                        existing_record.taluk = taluk_name
                        existing_record.ts_so_no = ts_so_no
                        existing_record.classification = classification
                        existing_record.sub_classification = sub_classification
                        existing_record.enchorochment = enchorochment
                        existing_record.hectare = hectare
                        existing_record.area = area
                        existing_record.sqm = sqm
                        existing_record.remarks = remarks
                        existing_record.street = street_name

                        existing_record.zone = normalize_value(zone)
                        existing_record.ward2 = normalize_value(ward)
                        existing_record.town_survey_no = normalize_value(town_survey_no)
                        existing_record.village_name = normalize_value(village_name)
                        existing_record.sub_division_no = normalize_value(sub_division_no)

                        existing_record.save()

                        pass


                    else:
                        # Create a ListOFValues instance and save it
                        # print("New Data Create")
                        river_name_id = ListOFValues.objects.get(list_of_values=row['river_name']).id

                        CadastralDeviation.objects.create(
                            unique_id=unique_id,
                            cadastral_master_id_id=river_name_id,
                            block=block_name,
                            ward=sub_basin,
                            district=district_name,
                            town=town_name,
                            taluk=taluk_name,
                            # asset_type=asset_type,
                            ts_so_no=ts_so_no,
                            classification=classification,
                            sub_classification=sub_classification,
                            enchorochment=enchorochment,
                            # buildings=buildings,
                            hectare=hectare,
                            area=area,
                            sqm=sqm,
                            remarks=remarks,
                            street=street_name,
                            dupcheck=dupcheck,
                            zone=zone,
                            ward2=ward,
                            town_survey_no=town_survey_no,
                            village_name=village_name,
                            sub_division_no=sub_division_no,
                        )

                        # obj.save()

                        id = CadastralDeviation.objects.last().id

                    child_existing_record = DeviationValue.objects.filter(dupcheck=child_dupcheck).first()

                    if child_existing_record:
                        existing_obj_count += 1

                        if enchrochment_type == 'Boun':

                            # obj_count1 += 1

                            point_id_value = 'point_id'
                            try:
                                query_obj = CadastralEntry.objects.get(unique_id=str(row[point_id_value]).strip())
                            except CadastralEntry.DoesNotExist:
                                response = {
                                    "error": f"No Boundary Pillar object found with unique id: {row[point_id_value]}"}
                                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
                            except CadastralEntry.MultipleObjectsReturned:
                                response = {
                                    "error": f"Multiple Boundary Pillar found with unique id: {row[point_id_value]}"}
                                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                            easting = 'easting'
                            try:
                                query_obj = CadastralEntry.objects.get(latitude=str(row[easting]).strip())
                            except CadastralEntry.DoesNotExist:
                                response = {"error": f"No Boundary Pillar object found with easting: {row[easting]}"}
                                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
                            except CadastralEntry.MultipleObjectsReturned:
                                response = {
                                    "error": f"Multiple Boundary Pillar found with easting: {row[easting]}"}
                                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                            northing = 'northing'
                            try:
                                query_obj = CadastralEntry.objects.get(longitude=str(row[northing]).strip())
                            except CadastralEntry.DoesNotExist:
                                response = {"error": f"No Boundary Pillar object found with northing: {row[northing]}"}
                                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
                            except CadastralEntry.MultipleObjectsReturned:
                                response = {
                                    "error": f"Multiple Boundary Pillar found with northing: {row[northing]}"}
                                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                            # point_type_id = ListOFValues.objects.get(list_of_values=row['point_type']).id

                            child_existing_record.point_id_id = CadastralEntry.objects.get(unique_id=point_id).id
                            child_existing_record.latitude = latitude
                            child_existing_record.longitude = longitude
                            child_existing_record.elevation = elevation
                            # point_type_id=point_type_id,
                            child_existing_record.cadastral_deviation_id = id
                            child_existing_record.save()
                        elif enchrochment_type == 'Ench':
                            print(f"Line {index+2}: {point_id}")
                            child_existing_record.point_id_2 = point_id
                            child_existing_record.latitude = latitude
                            child_existing_record.longitude = longitude
                            child_existing_record.elevation = elevation
                            # point_type_id=point_type_id,
                            child_existing_record.cadastral_deviation_id = id
                            child_existing_record.save()

                        elif enchrochment_type == "Cad":
                            # obj_count3 += 1

                            child_existing_record.point_id_2 = point_id
                            child_existing_record.latitude = latitude
                            child_existing_record.longitude = longitude
                            child_existing_record.elevation = elevation
                            child_existing_record.cadastral_deviation_id = id
                            child_existing_record.save()

                    else:

                        if enchrochment_type == 'Boun':

                            obj_count1 += 1

                            point_id_value = 'point_id'
                            try:
                                query_obj = CadastralEntry.objects.get(unique_id=str(row[point_id_value]).strip())
                            except CadastralEntry.DoesNotExist:
                                response = {
                                    "error": f"No Boundary Pillar object found with unique id: {row[point_id_value]}"}
                                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
                            except CadastralEntry.MultipleObjectsReturned:
                                response = {
                                    "error": f"Multiple Boundary Pillar found with unique id: {row[point_id_value]}"}
                                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                            easting = 'easting'
                            try:
                                query_obj = CadastralEntry.objects.get(latitude=str(row[easting]).strip())
                            except CadastralEntry.DoesNotExist:
                                response = {"error": f"No Boundary Pillar object found with easting: {row[easting]}"}
                                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
                            except CadastralEntry.MultipleObjectsReturned:
                                response = {
                                    "error": f"Multiple Boundary Pillar found with easting: {row[easting]}"}
                                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                            northing = 'northing'
                            try:
                                query_obj = CadastralEntry.objects.get(longitude=str(row[northing]).strip())
                            except CadastralEntry.DoesNotExist:
                                response = {"error": f"No Boundary Pillar object found with northing: {row[northing]}"}
                                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
                            except CadastralEntry.MultipleObjectsReturned:
                                response = {
                                    "error": f"Multiple Boundary Pillar found with northing: {row[northing]}"}
                                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                            # point_type_id = ListOFValues.objects.get(list_of_values=row['point_type']).id

                            try:
                                DeviationValue.objects.create(
                                    point_id_id=CadastralEntry.objects.get(unique_id=point_id).id,
                                    latitude=latitude,
                                    longitude=longitude,
                                    elevation=elevation,
                                    # point_type_id=point_type_id,
                                    cadastral_deviation_id=id,
                                    dupcheck=child_dupcheck
                                )
                            except IntegrityError as e:
                                detail_message = str(e).split("DETAIL:")[1].strip()
                                response = {"error": f"""
                                Error Line : {index+2}
                                Duplicate value 
                                 DETAIL:  {detail_message}
                                 """}
                                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                        elif enchrochment_type == 'Ench':
                            obj_count2 += 1
                            # point_type_id = ListOFValues.objects.get(list_of_values=row['point_type']).id
                            # print("Else condition working")
                            try:
                                DeviationValue.objects.create(
                                    point_id_2=point_id,
                                    latitude=latitude,
                                    longitude=longitude,
                                    elevation=elevation,
                                    # point_type_id=point_type_id,
                                    cadastral_deviation_id=id,
                                    dupcheck=child_dupcheck
                                )
                            except IntegrityError as e:
                                detail_message = str(e).split("DETAIL:")[1].strip()
                                response = {"error": f"""
                                 Error Line : {index+2}
                                Duplicate value 
                                 DETAIL:  {detail_message}
                                 """}
                                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                            except Exception as e:
                                # detail_message = str(e).split("DETAIL:")[1].strip()
                                response = {"error": f"""Error Line : "{index + 2}" 
                                                                 DETAIL:  {e}
                                                                 """}
                                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                        elif enchrochment_type == 'Cad':
                            obj_count3 += 1
                            # point_type_id = ListOFValues.objects.get(list_of_values=row['point_type']).id
                            # print("Else condition working")
                            try:
                                cad_obj = CadastralMaster.objects.filter(unique_id=point_id)
                                if not cad_obj:
                                    response = {"error": f""" Error Line : "{index + 2}"
                                     Message : "{point_id}" is missing this value in cadastral line.
                                                                     """}
                                    return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                                # print(point_id)

                                _deviation = DeviationValue(
                                    point_id_2=point_id,
                                    latitude=latitude,
                                    longitude=longitude,
                                    elevation=elevation,
                                    # point_type_id=point_type_id,
                                    cadastral_deviation_id=id,
                                    dupcheck=child_dupcheck
                                )
                                _deviation.save()
                            except IntegrityError as e:
                                detail_message = str(e).split("DETAIL:")[1].strip()
                                response = {"error": f"""
                                 Error Line : {index+2}
                                Duplicate value 
                                 DETAIL:  {detail_message}
                                 """}
                                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
                            except Exception as e:
                                print(e)

                except (CadastralEntry.DoesNotExist, ListOFValues.DoesNotExist) as e:
                    error_row = index + 2

                    if isinstance(e, ListOFValues.DoesNotExist):
                        error_message = f"Row: {error_row}, Wrong Data: 'List of Values matching query does not exist.'"
                    else:
                        error_message = f"Row: {error_row}, Wrong Data: 'Boundary Pillar matching query does not exist.'"

                    response = {"error": error_message}
                    return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

            response = {
                "Status": "Imported Successfully",
                "total_rows": total_rows,
                "create_obj_count": int(obj_count1) + int(obj_count2) + int(obj_count3),
                "existing_obj_count": existing_obj_count
            }
            return Response(data=response, status=status.HTTP_201_CREATED)

        except KeyError as e:
            error_message = f"Column '{e.args[0]}' not found in the Excel file."
            response = {"error": error_message}
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def intrusion_excel_import(request: Request):
    if request.method == 'POST':

        obj_count1 = 0
        obj_count2 = 0
        obj_count3 = 0
        existing_obj_count = 0

        uploaded_file = request.data.get('excel_file')
        if not uploaded_file or not uploaded_file.name.endswith('.xls') and not uploaded_file.name.endswith('.xlsx'):
            response = {"error": "Please upload a valid Excel file."}
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        serializer = IntrusionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        obj = IntrusionMasterExcelTable.objects.last()
        uploaded_file_path = obj.excel_file.path

        try:
            # Assuming you are using pandas to read the Excel file
            df = pd.read_excel(uploaded_file_path)
            # print(df)

            # Normalize column names to lowercase and remove spaces
            df.columns = df.columns.str.lower().str.replace(' ', '_')
            df = df.fillna('NA')

            total_rows = len(df)

            # Assuming your DataFrame has columns like 'list_type' and 'list_of_values'
            for index, row in df.iterrows():
                try:

                    # print(river_name_id)
                    unique_id = row['unique_id']
                    river_name = row['river_name']
                    block_name = row['block_name']
                    sub_basin = row['sub_basin']
                    district_name = row['district_name']
                    town_name = row['town_name']
                    taluk_name = row['taluk_name']
                    street_name = row['street_name']
                    ts_so_no = row['survey_no']
                    classification = row['classification']
                    sub_classification = row['sub_classification']
                    # asset_type = row['asset_type']
                    hectare = row['hectare']
                    area = row['ares']
                    sqm = row['sqm']
                    # buildings = row['buildings']
                    # no_of_buildings = row['no_of_buildings']
                    # no_of_floors = row['no_of_floors']
                    # usage_of_build = row['usage_of_build']
                    # occupier_name = row['occupier_name']
                    enchorochment = row['enchrochment']
                    remarks = row['remarks']

                    enchrochment_type = row['enchrochment_type'].strip()
                    # print(enchrochment_type)

                    point_id = row['point_id']

                    latitude = row['easting']
                    longitude = row['northing']
                    elevation = row['elevation']

                    zone = row['zone']
                    ward = row['ward']
                    town_survey_no = row['town_survey_no']
                    village_name = row['village_name']
                    sub_division_no = row['sub_div_no']
                    # point_type = row['point_type']
                    # point_type_id = ListOFValues.objects.get(list_of_values=row['point_type']).id

                    query_list = [
                        'river_name', 'block_name',
                        'sub_basin', 'district_name', 'town_name', 'taluk_name',
                        'classification', 'sub_classification'

                    ]
                    # print(taluk_name)
                    for query in query_list:
                        try:
                            if query == "town_name":
                                query_obj = ListOFValues.objects.get(list_of_values=str(row[query]).strip(),
                                                                     list_type__list_type="Town")
                            elif query == "taluk_name":
                                query_obj = ListOFValues.objects.get(list_of_values=str(row[query]).strip(),
                                                                     list_type__list_type="Taluk")
                            elif query == "block_name":
                                query_obj = ListOFValues.objects.get(list_of_values=str(row[query]).strip(),
                                                                     list_type__list_type="Block")
                            else:
                                query_obj = ListOFValues.objects.get(list_of_values=str(row[query]).strip())

                        except ListOFValues.DoesNotExist:
                            response = {"error": f""" Error Line : "{index + 2}"
                            Not found {query} in ListOFValues: {row[query]}"""}
                            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
                        except ListOFValues.MultipleObjectsReturned:
                            response = {"error": f""" Error Line : "{index + 2}"
                            Multiple ListOFValues objects found with {query}: {row[query]}"""}
                            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                    street_list = ['street_name']

                    for street_obj in street_list:
                        try:
                            query_obj = SurveyMaster.objects.filter(street_name=str(row[street_obj]).strip())
                            if not query_obj:
                                response = {"error": f""" Error Line : "{index + 2}"
                                No Street object found with {street_obj}: {row[street_obj]}"""}
                                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
                        except SurveyMaster.DoesNotExist:
                            response = {"error": f""" Error Line : "{index + 2}"
                            No Street object found with {street_obj}: {row[street_obj]}"""}
                            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
                        # except SurveyMaster.MultipleObjectsReturned:
                        #     response = {"error": f"Multiple Street objects found with {street_obj}: {row[street_obj]}"}
                        #     return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                    # survey_no = 'survey_no'
                    # try:
                    #     query_obj = SurveyMaster.objects.filter(survey_no=str(row[survey_no]).strip())
                    #     if not query_obj:
                    #         response = {"error": f""" Error Line : "{index + 2}"
                    #         No Street object found with {survey_no}: {row[survey_no]}"""}
                    #         return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
                    # except SurveyMaster.DoesNotExist:
                    #     response = {"error": f""" Error Line : "{index + 2}"
                    #     No Street object found with {survey_no}: {row[survey_no]}"""}
                    #     return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                    # print(point_type_id)

                    dupcheck = f"{unique_id}"
                    # print(dupcheck)
                    child_dupcheck = f"{latitude}{longitude}"

                    existing_record = IntrusionMaster.objects.filter(unique_id=unique_id).first()

                    if existing_record:
                        id = existing_record.id
                        # print(id)
                        river_name_id = ListOFValues.objects.get(list_of_values=row['river_name']).id

                        existing_record.unique_id = unique_id
                        existing_record.cadastral_master_id_id = river_name_id
                        existing_record.block = block_name
                        existing_record.ward = sub_basin
                        existing_record.district = district_name
                        existing_record.town = town_name
                        existing_record.taluk = taluk_name
                        existing_record.ts_so_no = ts_so_no
                        existing_record.classification = classification
                        existing_record.sub_classification = sub_classification
                        existing_record.enchorochment = enchorochment
                        existing_record.hectare = hectare
                        existing_record.area = area
                        existing_record.sqm = sqm
                        existing_record.remarks = remarks
                        existing_record.street = street_name

                        existing_record.zone = normalize_value(zone)
                        existing_record.ward2 = normalize_value(ward)
                        existing_record.town_survey_no = normalize_value(town_survey_no)
                        existing_record.village_name = normalize_value(village_name)
                        existing_record.sub_division_no = normalize_value(sub_division_no)

                        existing_record.save()
                        pass

                    else:
                        # Create a ListOFValues instance and save it
                        # print("New Data Create")
                        river_name_id = ListOFValues.objects.get(list_of_values=row['river_name']).id
                        IntrusionMaster.objects.create(
                            unique_id=unique_id,
                            cadastral_master_id_id=river_name_id,
                            block=block_name,
                            ward=sub_basin,
                            district=district_name,
                            town=town_name,
                            taluk=taluk_name,
                            # asset_type=asset_type,
                            ts_so_no=ts_so_no,
                            classification=classification,
                            sub_classification=sub_classification,
                            # no_of_buildings=no_of_buildings,
                            # no_of_floors=no_of_floors,
                            # usage_of_build=usage_of_build,
                            # occupier_name=occupier_name,
                            enchorochment=enchorochment,
                            # buildings=buildings,
                            hectare=hectare,
                            area=area,
                            sqm=sqm,
                            remarks=remarks,
                            street=street_name,
                            dupcheck=dupcheck,
                            zone=zone,
                            ward2=ward,
                            town_survey_no=town_survey_no,
                            village_name=village_name,
                            sub_division_no=sub_division_no,
                        )

                        # obj.save()

                        id = IntrusionMaster.objects.last().id

                    child_existing_record = IntrusionChild.objects.filter(dupcheck=child_dupcheck).first()

                    if child_existing_record:
                        existing_obj_count += 1
                        if enchrochment_type == 'Boun':

                            # obj_count1 += 1

                            point_id_value = 'point_id'
                            try:
                                query_obj = CadastralEntry.objects.get(unique_id=str(row[point_id_value]).strip())
                            except CadastralEntry.DoesNotExist:
                                response = {
                                    "error": f""" Error Line : "{index + 2}"
                                    No Boundary Pillar object found with unique id: {row[point_id_value]}"""}
                                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
                            except CadastralEntry.MultipleObjectsReturned:
                                response = {
                                    "error": f""" Error Line : "{index + 2}"
                                    Multiple Boundary Pillar found with unique id: {row[point_id_value]}"""}
                                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                            easting = 'easting'
                            try:
                                query_obj = CadastralEntry.objects.get(latitude=str(row[easting]).strip())
                            except CadastralEntry.DoesNotExist:
                                response = {"error": f""" Error Line : "{index + 2}"
                                No Boundary Pillar object found with easting: {row[easting]}"""}
                                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
                            except CadastralEntry.MultipleObjectsReturned:
                                response = {
                                    "error": f""" Error Line : "{index + 2}"
                                    Multiple Boundary Pillar found with easting: {row[easting]}"""}
                                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                            northing = 'northing'
                            try:
                                query_obj = CadastralEntry.objects.get(longitude=str(row[northing]).strip())
                            except CadastralEntry.DoesNotExist:
                                response = {"error": f""" Error Line : "{index + 2}"
                                No Boundary Pillar object found with northing: {row[northing]}"""}
                                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
                            except CadastralEntry.MultipleObjectsReturned:
                                response = {
                                    "error": f""" Error Line : "{index + 2}"
                                    Multiple Boundary Pillar found with northing: {row[northing]}"""}
                                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                            # point_type_id = ListOFValues.objects.get(list_of_values=row['point_type']).id

                            child_existing_record.point_id_id = CadastralEntry.objects.get(unique_id=point_id).id
                            child_existing_record.latitude = latitude
                            child_existing_record.longitude = longitude
                            child_existing_record.elevation = elevation
                            # point_type_id=point_type_id,
                            child_existing_record.cadastral_deviation_id = id
                            child_existing_record.save()
                        elif enchrochment_type == 'Intr':
                            # obj_count2 += 1
                            # point_type_id = ListOFValues.objects.get(list_of_values=row['point_type']).id
                            # print("Else condition working")

                            child_existing_record.point_id_2 = point_id
                            child_existing_record.latitude = latitude
                            child_existing_record.longitude = longitude
                            child_existing_record.elevation = elevation
                            # point_type_id=point_type_id,
                            child_existing_record.cadastral_deviation_id = id
                            child_existing_record.save()
                        elif enchrochment_type == 'Cad':
                            # obj_count3 += 1
                            child_existing_record.point_id_2 = point_id
                            child_existing_record.latitude = latitude
                            child_existing_record.longitude = longitude
                            child_existing_record.elevation = elevation
                            child_existing_record.cadastral_deviation_id = id
                            child_existing_record.save()

                    else:

                        if enchrochment_type == 'Boun':

                            obj_count1 += 1

                            point_id_value = 'point_id'
                            try:
                                query_obj = CadastralEntry.objects.get(unique_id=str(row[point_id_value]).strip())
                            except CadastralEntry.DoesNotExist:
                                response = {
                                    "error": f""" Error Line : "{index + 2}"
                                    No Boundary Pillar object found with unique id: {row[point_id_value]}"""}
                                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
                            except CadastralEntry.MultipleObjectsReturned:
                                response = {
                                    "error": f""" Error Line : "{index + 2}"
                                    Multiple Boundary Pillar found with unique id: {row[point_id_value]}"""}
                                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                            easting = 'easting'
                            try:
                                query_obj = CadastralEntry.objects.get(latitude=str(row[easting]).strip())
                            except CadastralEntry.DoesNotExist:
                                response = {"error": f""" Error Line : "{index + 2}"
                                No Boundary Pillar object found with easting: {row[easting]}"""}
                                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
                            except CadastralEntry.MultipleObjectsReturned:
                                response = {
                                    "error": f""" Error Line : "{index + 2}"
                                    Multiple Boundary Pillar found with easting: {row[easting]}"""}
                                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                            northing = 'northing'

                            try:
                                query_obj = CadastralEntry.objects.get(longitude=str(row[northing]).strip())
                            except CadastralEntry.DoesNotExist:
                                response = {"error": f""" Error Line : "{index + 2}"
                                No Boundary Pillar object found with northing: {row[northing]}"""}
                                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
                            except CadastralEntry.MultipleObjectsReturned:
                                response = {
                                    "error": f""" Error Line : "{index + 2}"
                                    Multiple Boundary Pillar found with northing: {row[northing]}"""}
                                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                            try:
                                IntrusionChild.objects.create(
                                    point_id_id=CadastralEntry.objects.get(unique_id=point_id).id,
                                    latitude=latitude,
                                    longitude=longitude,
                                    elevation=elevation,
                                    # point_type_id=point_type_id,
                                    intrusion_master_id=id,
                                    dupcheck=child_dupcheck
                                )
                            except IntegrityError as e:
                                detail_message = str(e).split("DETAIL:")[1].strip()
                                response = {"error": f""" Error Line : "{index + 2}"
                                Duplicate value 
                                 DETAIL:  {detail_message}
                                 """}
                        elif enchrochment_type == 'Intr':

                            obj_count2 += 1
                            # print("Else condition working")
                            try:
                                IntrusionChild.objects.create(
                                    point_id_2=point_id,
                                    latitude=latitude,
                                    longitude=longitude,
                                    elevation=elevation,
                                    # point_type_id=point_type_id,
                                    intrusion_master_id=id,
                                    dupcheck=child_dupcheck
                                )
                            except IntegrityError as e:
                                detail_message = str(e).split("DETAIL:")[1].strip()
                                response = {"error": f""" Error Line : "{index + 2}"
                                Duplicate value 
                                 DETAIL:  {detail_message}
                                 """}
                        elif enchrochment_type == 'Cad':

                            obj_count3 += 1
                            # print("Else condition working")
                            try:
                                cad_obj = CadastralMaster.objects.filter(unique_id=point_id)
                                if not cad_obj:
                                    response = {"error": f""" Error Line : "{index + 2}"
                                                                    Message : "{point_id}" is missing this value in cadastral line.
                                                                                                    """}
                                    return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                                IntrusionChild.objects.create(
                                    point_id_2=point_id,
                                    latitude=latitude,
                                    longitude=longitude,
                                    elevation=elevation,
                                    # point_type_id=point_type_id,
                                    intrusion_master_id=id,
                                    dupcheck=child_dupcheck
                                )
                            except IntegrityError as e:
                                detail_message = str(e).split("DETAIL:")[1].strip()
                                response = {"error": f""" Error Line : "{index + 2}"
                                Duplicate value 
                                 DETAIL:  {detail_message}
                                 """}
                                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                except (CadastralEntry.DoesNotExist, ListOFValues.DoesNotExist) as e:
                    error_row = index + 2

                    if isinstance(e, ListOFValues.DoesNotExist):
                        error_message = f"Row: {error_row}, Wrong Data: 'List of Values matching query does not exist.'"
                    else:
                        error_message = f"Row: {error_row}, Wrong Data: 'Boundary Pillar matching query does not exist.'"

                    response = {"error": error_message}
                    return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

            response = {
                "Status": "Imported Successfully",
                "total_rows": total_rows,
                "create_obj_count": int(obj_count1) + int(obj_count2) + int(obj_count3),
                "existing_obj_count": existing_obj_count
            }
            return Response(data=response, status=status.HTTP_201_CREATED)

        except KeyError as e:
            error_message = f"Column '{e.args[0]}' not found in the Excel file."
            response = {"error": error_message}
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def CL_river_list(request: Request):
    obj = CadastralMasterKMLTable.objects.all()
    serializer = CadastralMasterKMLTableSerializer(instance=obj, many=True)

    response = {"CadastralLine_Rivers": serializer.data}
    return Response(data=response, status=status.HTTP_200_OK)


@api_view(['GET'])
def boundary_river_list(request: Request):
    obj = BoundaryKMLTable.objects.all()
    serializer = BoundaryPillarTableSerializer(instance=obj, many=True)

    response = {"BoundaryPillar_Rivers": serializer.data}
    return Response(data=response, status=status.HTTP_200_OK)
@api_view(['GET'])
def enchrochment_river_list(request: Request):
    obj = EnchrochKMLTable.objects.all()
    serializer = EnchrochmentTableSerializer(instance=obj, many=True)
    response = {"Enchrochment_Rivers": serializer.data}
    return Response(data=response, status=status.HTTP_200_OK)

@api_view(['GET'])
def intrusion_river_list(request: Request):
    obj = IntrusionKMLTable.objects.all()
    serializer = IntrusionTableSerializer(instance=obj, many=True)

    response = {"Intrusion_Rivers": serializer.data}
    return Response(data=response, status=status.HTTP_200_OK)