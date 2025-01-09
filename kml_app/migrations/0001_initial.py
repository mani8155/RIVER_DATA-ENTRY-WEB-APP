# Generated by Django 4.2.7 on 2024-06-04 06:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CadastralDeviation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('district', models.CharField(blank=True, max_length=200, null=True)),
                ('taluk', models.CharField(blank=True, max_length=200, null=True)),
                ('town', models.CharField(blank=True, max_length=200, null=True)),
                ('revenue_ward_no', models.CharField(blank=True, max_length=200, null=True)),
                ('ts_so_no', models.CharField(blank=True, max_length=200, null=True)),
                ('classification', models.CharField(blank=True, max_length=200, null=True)),
                ('sub_classification', models.CharField(blank=True, max_length=200, null=True)),
                ('enchorochment', models.CharField(blank=True, max_length=200, null=True)),
                ('river_instruction', models.CharField(blank=True, max_length=200, null=True)),
                ('hectare', models.CharField(blank=True, max_length=200, null=True)),
                ('area', models.CharField(blank=True, max_length=200, null=True)),
                ('sqm', models.CharField(blank=True, max_length=200, null=True)),
                ('remarks', models.CharField(blank=True, max_length=200, null=True)),
                ('unique_id', models.CharField(max_length=200, unique=True)),
                ('river_id', models.CharField(blank=True, max_length=200)),
                ('upload_file', models.FileField(blank=True, null=True, upload_to='deviations/')),
                ('street', models.CharField(blank=True, max_length=200, null=True)),
                ('ward', models.CharField(blank=True, max_length=200, null=True)),
                ('block', models.CharField(blank=True, max_length=200, null=True)),
                ('dupcheck', models.TextField(max_length=400, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CadastralDeviationExcelTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('excel_file', models.FileField(blank=True, null=True, upload_to='enchrochments_excels/')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CadastralEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.CharField(max_length=200, unique=True)),
                ('sub_bassin', models.CharField(blank=True, max_length=200, null=True)),
                ('town', models.CharField(blank=True, max_length=200, null=True)),
                ('taluk', models.CharField(blank=True, max_length=200, null=True)),
                ('district', models.CharField(blank=True, max_length=200, null=True)),
                ('block', models.CharField(blank=True, max_length=200, null=True)),
                ('tsno_sdno', models.CharField(blank=True, max_length=200, null=True)),
                ('classify', models.CharField(blank=True, max_length=200, null=True)),
                ('sub_classify', models.CharField(blank=True, max_length=200, null=True)),
                ('latitude', models.FloatField(unique=True)),
                ('longitude', models.FloatField(unique=True)),
                ('elevation', models.CharField(blank=True, max_length=200, null=True)),
                ('type_of_pillar', models.CharField(blank=True, max_length=200, null=True)),
                ('photos', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('remarks', models.CharField(blank=True, max_length=200, null=True)),
                ('street', models.CharField(blank=True, max_length=200, null=True)),
                ('r_ward', models.CharField(blank=True, max_length=200, null=True)),
                ('dupcheck', models.TextField(max_length=400, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CadastralEntryExcelTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('excel_file', models.FileField(blank=True, null=True, upload_to='boundary_pillar_excels/')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CadastralMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taluk', models.CharField(blank=True, max_length=200, null=True)),
                ('block', models.CharField(blank=True, max_length=200, null=True)),
                ('district', models.CharField(blank=True, max_length=200, null=True)),
                ('town', models.CharField(blank=True, max_length=200, null=True)),
                ('sub_bassin', models.CharField(blank=True, max_length=200, null=True)),
                ('survey_no', models.CharField(blank=True, max_length=200, null=True)),
                ('file_upload', models.FileField(blank=True, null=True, upload_to='files/')),
                ('unique_id', models.CharField(max_length=200, unique=True)),
                ('dupcheck', models.TextField(max_length=400, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CadastralMasterExcelTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('excel_file', models.FileField(blank=True, null=True, upload_to='cadstal_line_excels/')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='IntrusionMasterExcelTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('excel_file', models.FileField(blank=True, null=True, upload_to='intrusion_excels/')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ListOFValues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('list_of_values', models.CharField(max_length=200)),
                ('active', models.BooleanField(default=True)),
                ('dupcheck', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ListofValuesExcelTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('excel_file', models.FileField(blank=True, null=True, upload_to='list_type_excels/')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ListType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('list_type', models.CharField(blank=True, max_length=200, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='StreetExcelTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('excel_file', models.FileField(blank=True, null=True, upload_to='street_excels/')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='StreetMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revenue_ward_no', models.CharField(blank=True, max_length=200, null=True)),
                ('dupcheck', models.CharField(max_length=200, unique=True)),
                ('block_name', models.ForeignKey(limit_choices_to={'list_type__list_type': 'Block'}, on_delete=django.db.models.deletion.CASCADE, related_name='block_name_entries', to='kml_app.listofvalues')),
                ('district_name', models.ForeignKey(limit_choices_to={'list_type__list_type': 'District'}, on_delete=django.db.models.deletion.CASCADE, related_name='district_name_entries', to='kml_app.listofvalues')),
                ('river_name', models.ForeignKey(limit_choices_to={'list_type__list_type': 'River Name'}, on_delete=django.db.models.deletion.CASCADE, related_name='river_name_entries', to='kml_app.listofvalues')),
                ('sub_basin', models.ForeignKey(limit_choices_to={'list_type__list_type': 'Subbasin'}, on_delete=django.db.models.deletion.CASCADE, related_name='sub_basin_entries', to='kml_app.listofvalues')),
                ('taluk_name', models.ForeignKey(limit_choices_to={'list_type__list_type': 'Taluk'}, on_delete=django.db.models.deletion.CASCADE, related_name='taluk_name_entries', to='kml_app.listofvalues')),
                ('town_name', models.ForeignKey(limit_choices_to={'list_type__list_type': 'Town'}, on_delete=django.db.models.deletion.CASCADE, related_name='town_name_entries', to='kml_app.listofvalues')),
            ],
        ),
        migrations.CreateModel(
            name='TalukMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taluk_name', models.CharField(max_length=200)),
                ('dupcheck', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WardRegion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ward_no', models.CharField(max_length=200, unique=True)),
                ('ward_name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TownMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('town_name', models.CharField(max_length=200)),
                ('ward_name', models.CharField(blank=True, max_length=200, null=True)),
                ('revenue_division_no', models.CharField(max_length=200)),
                ('dupcheck', models.CharField(blank=True, max_length=200, null=True)),
                ('district_name', models.ForeignKey(limit_choices_to={'list_type__list_type': 'District'}, on_delete=django.db.models.deletion.CASCADE, related_name='districts_name_entries', to='kml_app.listofvalues')),
                ('taluk_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kml_app.talukmaster')),
            ],
        ),
        migrations.AddField(
            model_name='talukmaster',
            name='ward_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kml_app.wardregion'),
        ),
        migrations.CreateModel(
            name='SurveyMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_name', models.CharField(blank=True, max_length=200, null=True)),
                ('survey_no', models.CharField(blank=True, max_length=200, null=True)),
                ('langitutte', models.FloatField(max_length=200, unique=True)),
                ('lattitude', models.FloatField(max_length=200, unique=True)),
                ('dupcheck', models.TextField(max_length=400, unique=True)),
                ('classification', models.ForeignKey(limit_choices_to={'list_type__list_type': 'Classification'}, on_delete=django.db.models.deletion.CASCADE, related_name='classification_name_entries', to='kml_app.listofvalues')),
                ('street_master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='street_master_set', to='kml_app.streetmaster')),
                ('sub_classification', models.ForeignKey(limit_choices_to={'list_type__list_type': 'Sub Classification'}, on_delete=django.db.models.deletion.CASCADE, related_name='sub_classification_name_entries', to='kml_app.listofvalues')),
            ],
        ),
        migrations.CreateModel(
            name='SubCadastralLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.CharField(blank=True, max_length=200, null=True)),
                ('long', models.CharField(blank=True, max_length=200, null=True)),
                ('dupcheck', models.TextField(max_length=400, unique=True)),
                ('cadastral', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cadastral_set', to='kml_app.cadastralmaster')),
            ],
        ),
        migrations.CreateModel(
            name='SubCadastralEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photos', models.ImageField(blank=True, null=True, upload_to='cadastral_piller_point/')),
                ('cadastral_entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kml_app.cadastralentry')),
            ],
        ),
        migrations.AddField(
            model_name='listofvalues',
            name='list_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kml_app.listtype'),
        ),
        migrations.CreateModel(
            name='IntrusionMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('district', models.CharField(blank=True, max_length=200, null=True)),
                ('taluk', models.CharField(blank=True, max_length=200, null=True)),
                ('town', models.CharField(blank=True, max_length=200, null=True)),
                ('revenue_ward_no', models.CharField(blank=True, max_length=200, null=True)),
                ('ts_so_no', models.CharField(blank=True, max_length=200, null=True)),
                ('classification', models.CharField(blank=True, max_length=200, null=True)),
                ('sub_classification', models.CharField(blank=True, max_length=200, null=True)),
                ('enchorochment', models.CharField(blank=True, max_length=200, null=True)),
                ('river_instruction', models.CharField(blank=True, max_length=200, null=True)),
                ('hectare', models.CharField(blank=True, max_length=200, null=True)),
                ('area', models.CharField(blank=True, max_length=200, null=True)),
                ('sqm', models.CharField(blank=True, max_length=200, null=True)),
                ('remarks', models.CharField(blank=True, max_length=200, null=True)),
                ('unique_id', models.CharField(max_length=200, unique=True)),
                ('river_id', models.CharField(blank=True, max_length=200)),
                ('upload_file', models.FileField(blank=True, null=True, upload_to='deviations/')),
                ('street', models.CharField(blank=True, max_length=200, null=True)),
                ('ward', models.CharField(blank=True, max_length=200, null=True)),
                ('block', models.CharField(blank=True, max_length=200, null=True)),
                ('dupcheck', models.TextField(max_length=400, unique=True)),
                ('cadastral_master_id', models.ForeignKey(limit_choices_to={'list_type__list_type': 'River Name'}, on_delete=django.db.models.deletion.PROTECT, related_name='river_entry', to='kml_app.listofvalues')),
            ],
        ),
        migrations.CreateModel(
            name='IntrusionKMLTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kml_file', models.FileField(blank=True, null=True, upload_to='intrusion_kml_files/')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('river_name', models.OneToOneField(limit_choices_to={'list_type__list_type': 'River Name'}, on_delete=django.db.models.deletion.PROTECT, to='kml_app.listofvalues')),
            ],
        ),
        migrations.CreateModel(
            name='IntrusionChild',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point_id_2', models.CharField(max_length=200, null=True, unique=True)),
                ('latitude', models.FloatField(unique=True)),
                ('longitude', models.FloatField(unique=True)),
                ('elevation', models.CharField(blank=True, max_length=200, null=True)),
                ('dupcheck', models.TextField(max_length=400, unique=True)),
                ('intrusion_master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intrusion_set', to='kml_app.intrusionmaster')),
                ('point_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='kml_app.cadastralentry')),
            ],
        ),
        migrations.CreateModel(
            name='EnchrochKMLTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kml_file', models.FileField(blank=True, null=True, upload_to='enchroch_kml_files/')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('river_name', models.OneToOneField(limit_choices_to={'list_type__list_type': 'River Name'}, on_delete=django.db.models.deletion.PROTECT, to='kml_app.listofvalues')),
            ],
        ),
        migrations.CreateModel(
            name='DeviationValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point_id_2', models.CharField(max_length=200, null=True, unique=True)),
                ('latitude', models.FloatField(unique=True)),
                ('longitude', models.FloatField(unique=True)),
                ('elevation', models.CharField(blank=True, max_length=200, null=True)),
                ('dupcheck', models.TextField(max_length=400, unique=True)),
                ('cadastral_deviation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cd_set', to='kml_app.cadastraldeviation')),
                ('point_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='kml_app.cadastralentry')),
            ],
        ),
        migrations.CreateModel(
            name='CadastralMasterKMLTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kml_file', models.FileField(blank=True, null=True, upload_to='cadstal_line_kml_files/')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('river_name', models.OneToOneField(limit_choices_to={'list_type__list_type': 'River Name'}, on_delete=django.db.models.deletion.PROTECT, to='kml_app.listofvalues')),
            ],
        ),
        migrations.AddField(
            model_name='cadastralmaster',
            name='river_name',
            field=models.ForeignKey(limit_choices_to={'list_type__list_type': 'River Name'}, on_delete=django.db.models.deletion.PROTECT, related_name='river', to='kml_app.listofvalues'),
        ),
        migrations.AddField(
            model_name='cadastralentry',
            name='river_bank',
            field=models.ForeignKey(limit_choices_to={'list_type__list_type': 'River Bank'}, on_delete=django.db.models.deletion.PROTECT, related_name='river_bank_entries', to='kml_app.listofvalues'),
        ),
        migrations.AddField(
            model_name='cadastralentry',
            name='river_name',
            field=models.ForeignKey(limit_choices_to={'list_type__list_type': 'River Name'}, on_delete=django.db.models.deletion.PROTECT, related_name='cadastral_river_name_entries', to='kml_app.listofvalues'),
        ),
        migrations.AddField(
            model_name='cadastraldeviation',
            name='cadastral_master_id',
            field=models.ForeignKey(limit_choices_to={'list_type__list_type': 'River Name'}, on_delete=django.db.models.deletion.PROTECT, related_name='river_entries', to='kml_app.listofvalues'),
        ),
        migrations.CreateModel(
            name='BoundaryKMLTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kml_file', models.FileField(blank=True, null=True, upload_to='boundary_kml_files/')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('river_name', models.OneToOneField(limit_choices_to={'list_type__list_type': 'River Name'}, on_delete=django.db.models.deletion.PROTECT, to='kml_app.listofvalues')),
            ],
        ),
        migrations.CreateModel(
            name='BlockMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('block_name', models.CharField(blank=True, max_length=200, null=True)),
                ('taluk_name', models.CharField(blank=True, max_length=200, null=True)),
                ('revenue_division_name', models.CharField(blank=True, max_length=200, null=True)),
                ('revenue_division_no', models.CharField(blank=True, max_length=200, null=True)),
                ('district_name', models.CharField(blank=True, max_length=200, null=True)),
                ('dub_check', models.CharField(blank=True, max_length=200, null=True)),
                ('ward_name', models.CharField(blank=True, max_length=200, null=True)),
                ('longitude', models.CharField(blank=True, max_length=200, null=True)),
                ('town_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kml_app.townmaster')),
            ],
        ),
    ]
