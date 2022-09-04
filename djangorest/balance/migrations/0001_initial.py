# Generated by Django 4.0 on 2022-09-04 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CoinType',
            fields=[
                ('simb', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=15, unique=True)),
            ],
            options={
                'verbose_name': 'CoinType',
                'verbose_name_plural': 'CoinTypes',
            },
        ),
    ]
