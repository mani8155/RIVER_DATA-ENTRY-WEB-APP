from rest_framework import serializers
from kml_app.models import *




class BoundaryPillarPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCadastralEntry
        fields = ['id', 'photos', 'cadastral_entry']






class ListTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListType
        fields = ["id", "list_type"]


class ListOfValuesSerializer(serializers.ModelSerializer):
    list_type_name = serializers.SerializerMethodField()

    class Meta:
        model = ListOFValues
        fields = ["id", "list_type", "list_type_name", "list_of_values", "active"]

    def get_list_type_name(self, obj):
        return str(obj.list_type)


# class CadastralLineKml(serializers.ModelSerializer):
#
#     class Meta:
#         model = CadastralMaster
#         fields = ["id", "river_name",  'file_upload', 'uid', 'unique_id']
#
#

class SurverySerializer(serializers.ModelSerializer):
    classification = serializers.SerializerMethodField()
    sub_classification = serializers.SerializerMethodField()

    class Meta:
        model = SurveyMaster
        fields = ["id", "street_name", "survey_no", "classification", "sub_classification", "langitutte", "lattitude"]

    def get_classification(self, obj):
        return str(obj.classification)

    def get_sub_classification(self, obj):
        return str(obj.classification)


class StreetSerializer(serializers.ModelSerializer):
    river_name = serializers.SerializerMethodField()
    block_name = serializers.SerializerMethodField()
    sub_basin = serializers.SerializerMethodField()
    district_name = serializers.SerializerMethodField()
    town_name = serializers.SerializerMethodField()
    taluk_name = serializers.SerializerMethodField()

    child = SurverySerializer(many=True, read_only=True, source='street_master_set')

    class Meta:
        model = StreetMaster
        fields = [
            'id', 'river_name', 'block_name',
            'sub_basin', 'district_name',
            'town_name', 'taluk_name', 'child']
        depth = 1  #

    def get_river_name(self, obj):
        return str(obj.river_name)

    def get_block_name(self, obj):
        return str(obj.block_name)

    def get_sub_basin(self, obj):
        return str(obj.sub_basin)

    def get_district_name(self, obj):
        return str(obj.district_name)

    def get_town_name(self, obj):
        return str(obj.town_name)

    def get_taluk_name(self, obj):
        return str(obj.taluk_name)


class SubCadastralLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCadastralLine
        fields = '__all__'


class CadastralMasterSerializer(serializers.ModelSerializer):
    child = SubCadastralLineSerializer(many=True, read_only=True, source='cadastral_set')
    river_name = serializers.SerializerMethodField()

    class Meta:
        model = CadastralMaster
        fields = ['id', 'unique_id', 'river_name', 'district','survey_no','zone','ward','town_survey_no','village_name',
                  'sub_division_no',
                  'town', 'taluk', 'block', 'child']

        depth = 1

    def get_river_name(self, obj):
        return str(obj.river_name)


class CadastralEntrySerializerForm(serializers.ModelSerializer):
    river_name = serializers.SerializerMethodField()
    river_bank = serializers.SerializerMethodField()

    class Meta:
        model = CadastralEntry
        fields = ["id", "unique_id", "river_name", "river_bank", "sub_bassin", "district",
                  "taluk", "town", "block", "street", "tsno_sdno", "latitude",'zone','ward','town_survey_no','village_name',
                  'sub_division_no',
                  "longitude", "classify", "sub_classify", "elevation", "type_of_pillar", "remarks"]

    def get_river_name(self, obj):
        return str(obj.river_name)

    def get_river_bank(self, obj):
        return str(obj.river_bank)


class DeviationValueSerializer(serializers.ModelSerializer):
    point_id = serializers.SerializerMethodField()
    # point_type = serializers.SerializerMethodField()

    class Meta:
        model = DeviationValue
        fields = [
            "id", "point_id", "point_id_2", "latitude", "longitude", "elevation"
        ]

    def get_point_id(self, obj):
        return str(obj.point_id)

    def get_point_type(self, obj):
        return str(obj.point_type)


class CadastralDeviationSerializerForm(serializers.ModelSerializer):
    child = DeviationValueSerializer(many=True, read_only=True, source="cd_set")

    river_name = serializers.SerializerMethodField()
    sub_bassin = serializers.SerializerMethodField()


    class Meta:
        model = CadastralDeviation
        fields = ["id", "unique_id", "river_name", "sub_bassin", "district",
                  "taluk", "town", "block", "street", "ts_so_no", "classification",
                  "sub_classification",  "hectare", "area", "sqm",
                  "enchorochment", "remarks",'zone','ward2','town_survey_no','village_name',
                  'sub_division_no',
                  "child"]
        depth = 1

    def get_river_name(self, obj):
        return str(obj.cadastral_master_id)

    def get_sub_bassin(self, obj):
        return str(obj.ward)



class IntrusionChildSerializer(serializers.ModelSerializer):
    point_id = serializers.SerializerMethodField()
    # point_type = serializers.SerializerMethodField()

    class Meta:
        model = IntrusionChild
        fields = [
            "id", "point_id", "point_id_2", "latitude", "longitude", "elevation"
        ]

    def get_point_id(self, obj):
        return str(obj.point_id)

    def get_point_type(self, obj):
        return str(obj.point_type)


class IntrusionMasterSerializer(serializers.ModelSerializer):
    child = IntrusionChildSerializer(many=True, read_only=True, source="intrusion_set")

    river_name = serializers.SerializerMethodField()
    sub_bassin = serializers.SerializerMethodField()

    class Meta:
        model = IntrusionMaster
        fields = ["id", "unique_id", "river_name", "sub_bassin", "district",
                  "taluk", "town", "block", "street", "ts_so_no", "classification",
                  "sub_classification",  "hectare", "area", "sqm", "enchorochment", "remarks",
                  'zone', 'ward2', 'town_survey_no', 'village_name', 'sub_division_no',
                  "child",

                  ]
        depth = 1

    def get_river_name(self, obj):
        return str(obj.cadastral_master_id)

    def get_sub_bassin(self, obj):
        return str(obj.ward)


class ListTypeExcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListofValuesExcelTable
        fields = ['excel_file']


class StreetExcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreetExcelTable
        fields = ['excel_file']


class CadastralMasterExcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CadastralMasterExcelTable
        fields = ['excel_file']


class CadastralEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CadastralEntryExcelTable
        fields = ['excel_file']


class CadastralDeviationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CadastralDeviationExcelTable
        fields = ['excel_file']


class IntrusionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntrusionMasterExcelTable
        fields = ['excel_file']


class CadastralMasterKMLTableSerializer(serializers.ModelSerializer):
    river_name = serializers.SerializerMethodField()
    class Meta:
        model = CadastralMasterKMLTable
        fields = ['river_name']

    def get_river_name(self, obj):
        return str(obj.river_name)

        # def get_river_name(self, obj):
        #     return str(obj.cadastral_master_id)

class BoundaryPillarTableSerializer(serializers.ModelSerializer):
    river_name = serializers.SerializerMethodField()
    class Meta:
        model = BoundaryKMLTable
        fields = ['river_name']

    def get_river_name(self, obj):
        return str(obj.river_name)

class EnchrochmentTableSerializer(serializers.ModelSerializer):
    river_name = serializers.SerializerMethodField()
    class Meta:
        model = EnchrochKMLTable
        fields = ['river_name']

    def get_river_name(self, obj):
        return str(obj.river_name)

class IntrusionTableSerializer(serializers.ModelSerializer):
    river_name = serializers.SerializerMethodField()
    class Meta:
        model = IntrusionKMLTable
        fields = ['river_name']

    def get_river_name(self, obj):
        return str(obj.river_name)