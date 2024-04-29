# Generated by Django 5.0.4 on 2024-04-28 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0006_alter_record_ingr_list'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempRecord',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ingr_list', models.TextField(verbose_name='Ingredient list')),
                ('conc_list', models.TextField(null=True, verbose_name='Concentration list')),
            ],
            options={
                'db_table': 'temp_records',
            },
        ),
        migrations.AddField(
            model_name='record',
            name='conc_list',
            field=models.TextField(null=True, verbose_name='Concentration list'),
        ),
        migrations.AlterField(
            model_name='record',
            name='ingr_list',
            field=models.TextField(verbose_name='Ingredient list'),
        ),
    ]
