# Generated by Django 4.2 on 2023-04-11 17:17

import base.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_categories_savedpassword'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', base.models.UserManager()),
            ],
        ),
    ]
