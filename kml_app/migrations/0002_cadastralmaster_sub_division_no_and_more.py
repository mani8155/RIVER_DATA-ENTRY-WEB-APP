# Generated by Django 4.2.7 on 2024-07-04 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kml_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cadastralmaster',
            name='sub_division_no',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='cadastralmaster',
            name='town_survey_no',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='cadastralmaster',
            name='village_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='cadastralmaster',
            name='ward',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='cadastralmaster',
            name='zone',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
