# Generated by Django 5.0.4 on 2024-04-30 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0007_temprecord_record_conc_list_alter_record_ingr_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='combination',
            name='comb_type',
            field=models.CharField(max_length=10),
        ),
    ]