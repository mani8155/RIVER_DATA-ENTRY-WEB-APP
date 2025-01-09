from urllib import request

from django import forms

from .models import *


class WardForm(forms.ModelForm):
    class Meta:
        model = WardRegion
        fields = ['ward_no', 'ward_name']

    def __init__(self, *args, **kwargs):
        super(WardForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class TalukForm(forms.ModelForm):
    class Meta:
        model = TalukMaster
        fields = ['taluk_name', 'ward_name']

    def __init__(self, *args, **kwargs):
        super(TalukForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class ListTypeForm(forms.ModelForm):
    class Meta:
        model = ListType
        fields = ['list_type']

    def __init__(self, *args, **kwargs):
        super(ListTypeForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class ListOFValuesForm(forms.ModelForm):
    class Meta:
        model = ListOFValues
        fields = ['list_type', 'list_of_values', 'active']

    def __init__(self, *args, **kwargs):
        super(ListOFValuesForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['active'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['list_type'].choices = [('', '-------select---------')] + list(self.fields['list_type'].choices)[1:]


class TownForm(forms.ModelForm):
    class Meta:
        model = TownMaster
        fields = [
            'revenue_division_no',
            'town_name',
            'taluk_name',
            'ward_name',
            'district_name']

    def __init__(self, *args, **kwargs):
        super(TownForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['ward_name'].widget.attrs.update({'readonly': ''})


class StreetForm(forms.ModelForm):
    class Meta:
        model = StreetMaster
        fields = ['river_name', 'sub_basin', 'district_name', 'taluk_name', 'town_name', 'block_name',
                  ]

    def __init__(self, *args, **kwargs):
        super(StreetForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class CadastralForm(forms.ModelForm):
    class Meta:
        model = CadastralEntry
        fields = [
            'unique_id', 'river_name', 'river_bank',
        ]

    def __init__(self, *args, **kwargs):
        super(CadastralForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        # self.fields['revenue_ward_no'].widget.attrs.update({'readonly': ''})
        # self.fields['taluk'].widget.attrs.update({'readonly': ''})
        # self.fields['district'].widget.attrs.update({'readonly': ''})
        # self.fields['sub_basin'].widget.attrs.update({'readonly': ''})
        # self.fields['town'].widget.attrs.update({'readonly': ''})
        # self.fields['block_name'].widget.attrs.update({'onchange': 'blockChange(this)'})
        self.fields['river_name'].widget.attrs.update({'onchange': 'SelectRiver(this)'})

        # self.fields['street'].widget.attrs.update({'onchange': 'SelectStreet(this)'})


class EditCadastralForm(forms.ModelForm):
    class Meta:
        model = CadastralEntry
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(EditCadastralForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['dupcheck'].required = False


class CadastralMasterForm(forms.ModelForm):
    class Meta:
        model = CadastralMaster
        fields = ['unique_id', 'river_name']
        # labels = {
        #     'unique_id': 'River Id'
        # }

    def __init__(self, *args, **kwargs):
        super(CadastralMasterForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['river_name'].widget.attrs.update({'onchange': 'SelectRiver(this)'})


class NewEditCadastralMasterForm(forms.ModelForm):
    class Meta:
        model = CadastralMaster
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(NewEditCadastralMasterForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['dupcheck'].required = False


class CadastralDeviationForm(forms.ModelForm):
    class Meta:
        model = CadastralDeviation
        fields = ['cadastral_master_id', 'unique_id']
        labels = {
            'cadastral_master_id': 'River Name',
            # 'area': 'Acre',
            # 'enchorochment': 'Enchorochment Area',
            # 'river_instruction': 'River Intrusion',

        }

        # fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CadastralDeviationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        # self.fields['revenue_ward_no'].widget.attrs.update({'readonly': ''})
        # self.fields['taluk'].widget.attrs.update({'readonly': ''})
        # self.fields['district'].widget.attrs.update({'readonly': ''})
        # self.fields['town'].widget.attrs.update({'readonly': ''})
        # # self.fields['river_id'].widget.attrs.update({'readonly': ''})
        # self.fields['street'].widget.attrs.update({'readonly': ''})
        # self.fields['ward'].widget.attrs.update({'readonly': ''})
        # self.fields['ts_so_no'].widget.attrs.update({'readonly': ''})
        # self.fields['classification'].widget.attrs.update({'readonly': ''})
        # self.fields['sub_classification'].widget.attrs.update({'readonly': ''})

        self.fields['cadastral_master_id'].choices = [('', '-----select-------')] + list(
            self.fields['cadastral_master_id'].choices)[1:]
        # self.fields['cadastral_entry'].choices = [('', '-----select-------')] + list(
        #     self.fields['cadastral_entry'].choices)[1:]
        self.fields['cadastral_master_id'].widget.attrs.update({'onchange': 'SelectRiver(this)'})


class NewEditCDForm(forms.ModelForm):
    class Meta:
        model = CadastralDeviation
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(NewEditCDForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['dupcheck'].required = False


class DeviationForm(forms.ModelForm):
    class Meta:
        model = DeviationValue
        fields = ['point_id', 'latitude', 'longitude', 'elevation']
        labels = {
            "latitude": "EASTING",
            "longitude": "NORTHING",
        }

    def __init__(self, *args, **kwargs):
        super(DeviationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['point_id'].widget.attrs.update({'onchange': 'PointId(this)'})


class DeviationForm2(forms.ModelForm):
    class Meta:
        model = DeviationValue
        fields = ['point_id_2', 'latitude', 'longitude', 'elevation']
        labels = {
            "point_id_2": "POINT ID",
            "latitude": "EASTING",
            "longitude": "NORTHING",
        }

    def __init__(self, *args, **kwargs):
        super(DeviationForm2, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class SubCadastralLineForm(forms.ModelForm):
    class Meta:
        model = SubCadastralLine
        fields = ['lat', 'long']
        labels = {
            'lat': 'EASTING',
            'long': 'NORTHING',
        }

    def __init__(self, *args, **kwargs):
        super(SubCadastralLineForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class BlockForm(forms.ModelForm):
    class Meta:
        model = BlockMaster
        fields = ['block_name', 'town_name', 'ward_name', 'taluk_name', 'revenue_division_no', 'district_name']

    def __init__(self, *args, **kwargs):
        super(BlockForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['revenue_division_no'].widget.attrs.update({'readonly': ''})
        self.fields['taluk_name'].widget.attrs.update({'readonly': ''})
        self.fields['district_name'].widget.attrs.update({'readonly': ''})
        self.fields['ward_name'].widget.attrs.update({'readonly': ''})


# ________________________________________________________________________________________________

class SurveyMasterForm(forms.ModelForm):
    class Meta:
        model = SurveyMaster
        fields = ['street_name', 'survey_no', 'classification', 'sub_classification', 'langitutte', 'lattitude']
        labels = {
            "langitutte": "EASTING",
            "lattitude": "NORTHING",
        }

    def __init__(self, *args, **kwargs):
        super(SurveyMasterForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class IntrusionForm(forms.ModelForm):
    class Meta:
        model = IntrusionMaster
        fields = ['cadastral_master_id', 'unique_id']
        labels = {
            'cadastral_master_id': 'River Name',
        }

    def __init__(self, *args, **kwargs):
        super(IntrusionForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['cadastral_master_id'].choices = [('', '-----select-------')] + list(
            self.fields['cadastral_master_id'].choices)[1:]
        self.fields['cadastral_master_id'].widget.attrs.update({'onchange': 'SelectRiver(this)'})


class EditIntrusionForm(forms.ModelForm):
    class Meta:
        model = IntrusionMaster
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EditIntrusionForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['dupcheck'].required = False


class IntrusionChildForm(forms.ModelForm):
    class Meta:
        model = IntrusionChild
        fields = ['point_id', 'latitude', 'longitude', 'elevation']
        labels = {
            "latitude": "EASTING",
            "longitude": "NORTHING",
        }

    def __init__(self, *args, **kwargs):
        super(IntrusionChildForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['point_id'].widget.attrs.update({'onchange': 'PointId(this)'})


class IntrusionChildForm2(forms.ModelForm):
    class Meta:
        model = IntrusionChild
        fields = ['point_id_2', 'latitude', 'longitude', 'elevation']
        labels = {
            "point_id_2": "POINT ID",
            "latitude": "EASTING",
            "longitude": "NORTHING",
        }

    def __init__(self, *args, **kwargs):
        super(IntrusionChildForm2, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class CM_KMl_FORM(forms.ModelForm):
    class Meta:
        model = CadastralMasterKMLTable
        fields = ['river_name', 'kml_file']

    def __init__(self, *args, **kwargs):
        super(CM_KMl_FORM, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['kml_file'].widget.attrs.update({'accept': '.kml, .kmz'})


class Ench_KMl_FORM(forms.ModelForm):
    class Meta:
        model = EnchrochKMLTable
        fields = ['river_name', 'kml_file']

    def __init__(self, *args, **kwargs):
        super(Ench_KMl_FORM, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['kml_file'].widget.attrs.update({'accept': '.kml, .kmz'})


class Intrusion_KMl_FORM(forms.ModelForm):
    class Meta:
        model = IntrusionKMLTable
        fields = ['river_name', 'kml_file']

    def __init__(self, *args, **kwargs):
        super(Intrusion_KMl_FORM, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['kml_file'].widget.attrs.update({'accept': '.kml, .kmz'})


class Boundary_KMl_FORM(forms.ModelForm):
    class Meta:
        model = BoundaryKMLTable
        fields = ['river_name', 'kml_file']

    def __init__(self, *args, **kwargs):
        super(Boundary_KMl_FORM, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['kml_file'].widget.attrs.update({'accept': '.kml, .kmz'})
