# Generated by Django 5.0.4 on 2024-05-27 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0009_alter_record_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skin',
            fields=[
                ('id_line', models.AutoField(primary_key=True, serialize=False)),
                ('ingredients', models.TextField(verbose_name='Ingredient list')),
                ('combination', models.IntegerField(null=True, verbose_name='Combination')),
                ('dry', models.IntegerField(null=True, verbose_name='Dry')),
                ('normal', models.IntegerField(null=True, verbose_name='Normal')),
                ('oily', models.IntegerField(null=True, verbose_name='Oily')),
                ('sensitive', models.IntegerField(null=True, verbose_name='Sensitive')),
            ],
        ),
    ]
