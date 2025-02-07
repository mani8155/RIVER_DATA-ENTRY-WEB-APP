# Generated by Django 4.2.7 on 2024-07-04 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kml_app', '0003_cadastralentry_sub_division_no_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cadastraldeviation',
            name='sub_division_no',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='cadastraldeviation',
            name='town_survey_no',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='cadastraldeviation',
            name='village_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='cadastraldeviation',
            name='zone',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
