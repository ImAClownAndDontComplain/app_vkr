# Generated by Django 5.0.4 on 2024-04-22 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0005_type_type_short_alter_type_type_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='ingr_list',
            field=models.TextField(verbose_name='List'),
        ),
    ]
