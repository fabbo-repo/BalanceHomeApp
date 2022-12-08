# Generated by Django 4.0.8 on 2022-12-08 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FrontendVersion',
            fields=[
                ('version', models.CharField(max_length=8, primary_key=True, serialize=False, verbose_name='version')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Frontend version',
                'verbose_name_plural': 'Frontend versions',
                'ordering': ['-created'],
            },
        ),
    ]
