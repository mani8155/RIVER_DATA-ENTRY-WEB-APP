from django.db import models
from django.db.models import Q



# class SettingsModel(models.Model):
#     application_name = models.CharField(max_length=200)
#     api_url = models.CharField(max_length=200)
#     favicon_caption = models.CharField(max_length=200)
#     favicon_logo = models.ImageField(upload_to='images/')
#
#     def __str__(self):
#         return self.application_name
# Create your models here.

class WardRegion(models.Model):
    #
    ward_no = models.CharField(max_length=200, unique=True)
    ward_name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.ward_name


class TalukMaster(models.Model):
    #
    # rev_division_no = models.CharField(max_length=200)
    taluk_name = models.CharField(max_length=200)
    ward_name = models.ForeignKey(WardRegion, on_delete=models.CASCADE)
    dupcheck = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.taluk_name)


class ListType(models.Model):
    #
    list_type = models.CharField(max_length=200, unique=True, blank=True, null=True)

    def __str__(self):
        return str(self.list_type)


class ListofValuesExcelTable(models.Model):

    excel_file = models.FileField(upload_to='list_type_excels/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)


class ListOFValues(models.Model):

    list_type = models.ForeignKey(ListType, on_delete=models.CASCADE)
    list_of_values = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    dupcheck = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.list_of_values


class TownMaster(models.Model):

    town_name = models.CharField(max_length=200)
    ward_name = models.CharField(max_length=200, null=True, blank=True)
    taluk_name = models.ForeignKey(TalukMaster, on_delete=models.CASCADE)
    # revenue_division_name = models.CharField(max_length=200)
    revenue_division_no = models.CharField(max_length=200)
    district_name = models.ForeignKey(ListOFValues, on_delete=models.CASCADE,
                                      limit_choices_to={'list_type__list_type': 'District'},
                                      related_name='districts_name_entries')
    dupcheck = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.town_name


class BlockMaster(models.Model):

    block_name = models.CharField(max_length=200, null=True, blank=True)
    town_name = models.ForeignKey(TownMaster, on_delete=models.CASCADE)
    taluk_name = models.CharField(max_length=200, null=True, blank=True)
    revenue_division_name = models.CharField(max_length=200, null=True, blank=True)
    revenue_division_no = models.CharField(max_length=200, null=True, blank=True)
    district_name = models.CharField(max_length=200, null=True, blank=True)
    dub_check = models.CharField(max_length=200, null=True, blank=True)
    ward_name = models.CharField(max_length=200, null=True, blank=True)
    longitude = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.block_name)


class StreetExcelTable(models.Model):

    excel_file = models.FileField(upload_to='street_excels/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)


class StreetMaster(models.Model):

    river_name = models.ForeignKey(ListOFValues, on_delete=models.CASCADE,
                                   limit_choices_to={'list_type__list_type': 'River Name'},
                                   related_name='river_name_entries')
    block_name = models.ForeignKey(ListOFValues, on_delete=models.CASCADE,
                                   limit_choices_to={'list_type__list_type': 'Block'},
                                   related_name='block_name_entries')
    sub_basin = models.ForeignKey(ListOFValues, on_delete=models.CASCADE,
                                  limit_choices_to={'list_type__list_type': 'Subbasin'},
                                  related_name='sub_basin_entries')
    district_name = models.ForeignKey(ListOFValues, on_delete=models.CASCADE,
                                      limit_choices_to={'list_type__list_type': 'District'},
                                      related_name='district_name_entries')
    town_name = models.ForeignKey(ListOFValues, on_delete=models.CASCADE,
                                  limit_choices_to={'list_type__list_type': 'Town'},
                                  related_name='town_name_entries')
    taluk_name = models.ForeignKey(ListOFValues, on_delete=models.CASCADE,
                                   limit_choices_to={'list_type__list_type': 'Taluk'},
                                   related_name='taluk_name_entries')
    revenue_ward_no = models.CharField(max_length=200, blank=True, null=True)
    dupcheck = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return str(self.river_name)


class SurveyMaster(models.Model):

    street_name = models.CharField(max_length=200, blank=True, null=True)
    survey_no = models.CharField(max_length=200, blank=True, null=True)
    classification = models.ForeignKey(ListOFValues, on_delete=models.CASCADE,
                                       limit_choices_to={'list_type__list_type': 'Classification'},
                                       related_name='classification_name_entries')
    sub_classification = models.ForeignKey(ListOFValues, on_delete=models.CASCADE,
                                           limit_choices_to={'list_type__list_type': 'Sub Classification'},
                                           related_name='sub_classification_name_entries')
    langitutte = models.FloatField(max_length=200, unique=True)
    lattitude = models.FloatField(max_length=200, unique=True)
    street_master = models.ForeignKey(StreetMaster, on_delete=models.CASCADE, related_name='street_master_set')
    dupcheck = models.TextField(max_length=400, unique=True)

    # classify = models.ForeignKey(ListOFValues, on_delete=models.CASCADE,
    #                              limit_choices_to={'list_type__list_type': 'Classification'},
    #                              related_name='classification_entries'
    #                              )
    #
    # sub_classify = models.ForeignKey(ListOFValues, on_delete=models.CASCADE,
    #                                  limit_choices_to={'list_type__list_type': 'Sub Classification'},
    #                                  related_name='sub_classification_entries'
    #                                  )

    def __str__(self):
        return str(self.street_name)


class CadastralMasterExcelTable(models.Model):

    excel_file = models.FileField(upload_to='cadstal_line_excels/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)


class CadastralMasterKMLTable(models.Model):

    river_name = models.OneToOneField(ListOFValues, on_delete=models.PROTECT,
                                      limit_choices_to={'list_type__list_type': 'River Name'})
    kml_file = models.FileField(upload_to='cadstal_line_kml_files/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)


class BoundaryKMLTable(models.Model):
    river_name = models.OneToOneField(ListOFValues, on_delete=models.PROTECT,
                                      limit_choices_to={'list_type__list_type': 'River Name'})
    kml_file = models.FileField(upload_to='boundary_kml_files/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)


class EnchrochKMLTable(models.Model):

    river_name = models.OneToOneField(ListOFValues, on_delete=models.PROTECT,
                                      limit_choices_to={'list_type__list_type': 'River Name'})
    kml_file = models.FileField(upload_to='enchroch_kml_files/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)


class IntrusionKMLTable(models.Model):

    river_name = models.OneToOneField(ListOFValues, on_delete=models.PROTECT,
                                      limit_choices_to={'list_type__list_type': 'River Name'})
    kml_file = models.FileField(upload_to='intrusion_kml_files/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)



class CadastralMaster(models.Model):

    # river_name = models.CharField(max_length=200, blank=True, null=True)
    river_name = models.ForeignKey(ListOFValues, on_delete=models.PROTECT,
                                   limit_choices_to={'list_type__list_type': 'River Name'},
                                   related_name='river')
    taluk = models.CharField(max_length=200, null=True, blank=True)
    block = models.CharField(max_length=200, null=True, blank=True)
    district = models.CharField(max_length=200, null=True, blank=True)
    town = models.CharField(max_length=200, null=True, blank=True)
    sub_bassin = models.CharField(max_length=200, null=True, blank=True)
    survey_no = models.CharField(max_length=200, null=True, blank=True)
    file_upload = models.FileField(upload_to='files/', blank=True, null=True)
    unique_id = models.CharField(max_length=200, unique=True)
    dupcheck = models.TextField(max_length=400, unique=True)
    zone = models.CharField(max_length=200, null=True, blank=True)
    ward = models.CharField(max_length=200, null=True, blank=True)
    town_survey_no = models.CharField(max_length=200, null=True, blank=True)
    village_name = models.CharField(max_length=200, null=True, blank=True)
    sub_division_no = models.CharField(max_length=200, null=True, blank=True)

    # seq = 0

    # def save(self, *args, **kwargs):
    #     if not self.uid:
    #         side = 'Riv'
    #         CadastralMaster.seq += 1
    #         self.uid = f'{side}{CadastralMaster.seq:03}'
    #
    #     super().save(*args, **kwargs)

    def __str__(self):
        return str(self.unique_id)


class SubCadastralLine(models.Model):

    # ward = models.CharField(max_length=200, null=True, blank=True)
    # taluk = models.CharField(max_length=200, null=True, blank=True)
    # town = models.CharField(max_length=200, null=True, blank=True)

    # block = models.CharField(max_length=200, null=True, blank=True)

    lat = models.CharField(max_length=200, null=True, blank=True)
    long = models.CharField(max_length=200, null=True, blank=True)
    cadastral = models.ForeignKey(CadastralMaster, on_delete=models.CASCADE, related_name='cadastral_set')
    dupcheck = models.TextField(max_length=400, unique=True)

    def __str__(self):
        return str(self.id)


class CadastralEntryExcelTable(models.Model):

    excel_file = models.FileField(upload_to='boundary_pillar_excels/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)


class CadastralEntry(models.Model):

    unique_id = models.CharField(max_length=200, unique=True)

    river_name = models.ForeignKey(ListOFValues, on_delete=models.PROTECT,
                                   limit_choices_to={'list_type__list_type': 'River Name'},
                                   related_name='cadastral_river_name_entries')

    river_bank = models.ForeignKey(ListOFValues, on_delete=models.PROTECT,
                                   limit_choices_to={'list_type__list_type': 'River Bank'},
                                   related_name='river_bank_entries'
                                   )

    sub_bassin = models.CharField(max_length=200, blank=True, null=True)
    town = models.CharField(max_length=200, blank=True, null=True)
    taluk = models.CharField(max_length=200, blank=True, null=True)
    district = models.CharField(max_length=200, blank=True, null=True)
    revenue_ward_no = models.CharField(max_length=200, blank=True, null=True),
    block = models.CharField(max_length=200, blank=True, null=True)
    tsno_sdno = models.CharField(max_length=200, blank=True, null=True)

    classify = models.CharField(max_length=200, blank=True, null=True)

    sub_classify = models.CharField(max_length=200, blank=True, null=True)

    latitude = models.FloatField(unique=True)
    longitude = models.FloatField(unique=True)
    elevation = models.CharField(max_length=200, blank=True, null=True)

    type_of_pillar = models.CharField(max_length=200, blank=True, null=True)

    photos = models.ImageField(blank=True, null=True, upload_to='images/')
    remarks = models.CharField(max_length=200, blank=True, null=True)
    street = models.CharField(max_length=200, blank=True, null=True)
    r_ward = models.CharField(max_length=200, blank=True, null=True)
    dupcheck = models.TextField(max_length=400, unique=True)
    zone = models.CharField(max_length=200, null=True, blank=True)
    ward = models.CharField(max_length=200, null=True, blank=True)
    town_survey_no = models.CharField(max_length=200, null=True, blank=True)
    village_name = models.CharField(max_length=200, null=True, blank=True)
    sub_division_no = models.CharField(max_length=200, null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         if self.river_bank and self.river_bank.list_of_values == 'Right':
    #             _type = CadastralEntry.objects.filter(river_bank__list_of_values='Right').order_by(
    #                 '-unique_id').first()
    #             if _type and _type.unique_id and _type.unique_id[3:].isdigit():
    #                 seq = int(_type.unique_id[3:]) + 1
    #             else:
    #                 seq = 1
    #             self.unique_id = f'R{seq:03}'
    #         else:
    #             _type = CadastralEntry.objects.filter(river_bank__list_of_values='Left').order_by(
    #                 '-unique_id').first()
    #             if _type and _type.unique_id and _type.unique_id[3:].isdigit():
    #                 seq = int(_type.unique_id[3:]) + 1
    #             else:
    #                 seq = 1
    #             self.unique_id = f'L{seq:03}'
    #
    #         # Call the original save method
    #         super().save(*args, **kwargs)
    #
    def __str__(self):
        return str(self.unique_id)


class SubCadastralEntry(models.Model):

    photos = models.ImageField(blank=True, null=True, upload_to='cadastral_piller_point/')
    cadastral_entry = models.ForeignKey(CadastralEntry, on_delete=models.CASCADE)


class CadastralDeviationExcelTable(models.Model):

    excel_file = models.FileField(upload_to='enchrochments_excels/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)


class CadastralDeviation(models.Model):

    # asset_type = models.CharField(max_length=200, null=True, blank=True)
    district = models.CharField(max_length=200, null=True, blank=True)
    taluk = models.CharField(max_length=200, null=True, blank=True)
    town = models.CharField(max_length=200, null=True, blank=True)
    revenue_ward_no = models.CharField(max_length=200, null=True, blank=True)
    ts_so_no = models.CharField(max_length=200, null=True, blank=True)
    classification = models.CharField(max_length=200, null=True, blank=True)
    sub_classification = models.CharField(max_length=200, null=True, blank=True)
    # no_of_buildings = models.CharField(max_length=200, null=True, blank=True)
    # no_of_floors = models.CharField(max_length=200, null=True, blank=True)
    # usage_of_build = models.CharField(max_length=200, null=True, blank=True)
    # occupier_name = models.CharField(max_length=200, null=True, blank=True)
    enchorochment = models.CharField(max_length=200, null=True, blank=True)
    river_instruction = models.CharField(max_length=200, null=True, blank=True)
    hectare = models.CharField(max_length=200, null=True, blank=True)
    area = models.CharField(max_length=200, null=True, blank=True)
    sqm = models.CharField(max_length=200, null=True, blank=True)
    remarks = models.CharField(max_length=200, null=True, blank=True)
    # cadastral_master_id = models.ForeignKey(CadastralMaster, on_delete=models.CASCADE)
    cadastral_master_id = models.ForeignKey(ListOFValues, on_delete=models.PROTECT,
                                            limit_choices_to={'list_type__list_type': 'River Name'},
                                            related_name='river_entries')
    # cadastral_entry = models.ForeignKey(CadastralEntry, on_delete=models.CASCADE)
    unique_id = models.CharField(max_length=200, unique=True)
    river_id = models.CharField(max_length=200, blank=True)
    # buildings = models.CharField(max_length=200, blank=True, null=True)
    upload_file = models.FileField(upload_to='deviations/', blank=True, null=True)
    street = models.CharField(max_length=200, blank=True, null=True)
    ward = models.CharField(max_length=200, blank=True, null=True)
    block = models.CharField(max_length=200, null=True, blank=True)
    dupcheck = models.TextField(max_length=400, unique=True)
    zone = models.CharField(max_length=200, null=True, blank=True)
    ward2 = models.CharField(max_length=200, null=True, blank=True)
    town_survey_no = models.CharField(max_length=200, null=True, blank=True)
    village_name = models.CharField(max_length=200, null=True, blank=True)
    sub_division_no = models.CharField(max_length=200, null=True, blank=True)

    # cadastral_pillar = models.ForeignKey(CadastralEntry, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.unique_id)


class DeviationValue(models.Model):
    point_id = models.ForeignKey(CadastralEntry, on_delete=models.PROTECT, blank=True, null=True)
    point_id_2 = models.CharField(max_length=200, unique=True, null=True)
    latitude = models.FloatField(unique=True)
    longitude = models.FloatField(unique=True)
    elevation = models.CharField(max_length=200, null=True, blank=True)
    # point_type = models.CharField(max_length=200, null=True, blank=True)
    # point_type = models.ForeignKey(ListOFValues, on_delete=models.PROTECT,
    #                                limit_choices_to={'list_type__list_type': 'Point Type'},
    #                                related_name='point_type_entries')
    cadastral_deviation = models.ForeignKey(CadastralDeviation, on_delete=models.CASCADE, related_name='cd_set')
    dupcheck = models.TextField(max_length=400, unique=True)

    def __str__(self):
        return f"{self.cadastral_deviation}|{self.latitude}"


class IntrusionMasterExcelTable(models.Model):
    excel_file = models.FileField(upload_to='intrusion_excels/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)


class IntrusionMaster(models.Model):
    # asset_type = models.CharField(max_length=200, null=True, blank=True)
    district = models.CharField(max_length=200, null=True, blank=True)
    taluk = models.CharField(max_length=200, null=True, blank=True)
    town = models.CharField(max_length=200, null=True, blank=True)
    revenue_ward_no = models.CharField(max_length=200, null=True, blank=True)
    ts_so_no = models.CharField(max_length=200, null=True, blank=True)
    classification = models.CharField(max_length=200, null=True, blank=True)
    sub_classification = models.CharField(max_length=200, null=True, blank=True)
    # no_of_buildings = models.CharField(max_length=200, null=True, blank=True)
    # no_of_floors = models.CharField(max_length=200, null=True, blank=True)
    # usage_of_build = models.CharField(max_length=200, null=True, blank=True)
    # occupier_name = models.CharField(max_length=200, null=True, blank=True)
    enchorochment = models.CharField(max_length=200, null=True, blank=True)
    river_instruction = models.CharField(max_length=200, null=True, blank=True)
    hectare = models.CharField(max_length=200, null=True, blank=True)
    area = models.CharField(max_length=200, null=True, blank=True)
    sqm = models.CharField(max_length=200, null=True, blank=True)
    remarks = models.CharField(max_length=200, null=True, blank=True)
    # cadastral_master_id = models.ForeignKey(CadastralMaster, on_delete=models.CASCADE)
    cadastral_master_id = models.ForeignKey(ListOFValues, on_delete=models.PROTECT,
                                            limit_choices_to={'list_type__list_type': 'River Name'},
                                            related_name='river_entry')
    # cadastral_entry = models.ForeignKey(CadastralEntry, on_delete=models.CASCADE)
    unique_id = models.CharField(max_length=200, unique=True)
    river_id = models.CharField(max_length=200, blank=True)
    # buildings = models.CharField(max_length=200, blank=True, null=True)
    upload_file = models.FileField(upload_to='deviations/', blank=True, null=True)
    street = models.CharField(max_length=200, blank=True, null=True)
    ward = models.CharField(max_length=200, blank=True, null=True)
    block = models.CharField(max_length=200, null=True, blank=True)
    dupcheck = models.TextField(max_length=400, unique=True)
    zone = models.CharField(max_length=200, null=True, blank=True)
    ward2 = models.CharField(max_length=200, null=True, blank=True)
    town_survey_no = models.CharField(max_length=200, null=True, blank=True)
    village_name = models.CharField(max_length=200, null=True, blank=True)
    sub_division_no = models.CharField(max_length=200, null=True, blank=True)

    # cadastral_pillar = models.ForeignKey(CadastralEntry, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.unique_id)


class IntrusionChild(models.Model):

    point_id = models.ForeignKey(CadastralEntry, on_delete=models.PROTECT, blank=True, null=True)
    point_id_2 = models.CharField(max_length=200, unique=True, null=True)
    latitude = models.FloatField(unique=True)
    longitude = models.FloatField(unique=True)
    elevation = models.CharField(max_length=200, null=True, blank=True)
    # point_type = models.CharField(max_length=200, null=True, blank=True)
    # point_type = models.ForeignKey(ListOFValues, on_delete=models.CASCADE,
    #                                limit_choices_to={'list_type__list_type': 'Point Type'},
    #                                related_name='point_type_entry')
    intrusion_master = models.ForeignKey(IntrusionMaster, on_delete=models.CASCADE, related_name='intrusion_set')
    dupcheck = models.TextField(max_length=400, unique=True)

    def __str__(self):
        return f"{self.intrusion_master}|{self.latitude}"



