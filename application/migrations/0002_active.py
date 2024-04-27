# Generated by Django 5.0.4 on 2024-04-19 08:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Active',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('low_conc', models.FloatField(null=True, verbose_name='Low concentration')),
                ('medium_conc', models.FloatField(null=True, verbose_name='Medium concentration')),
                ('high_conc', models.FloatField(null=True, verbose_name='High concentration')),
                ('inci_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.inci', verbose_name='INCI')),
            ],
            options={
                'db_table': 'active',
            },
        ),
    ]
