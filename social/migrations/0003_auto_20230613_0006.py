# Generated by Django 3.1.2 on 2023-06-12 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0002_auto_20230612_2347'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userpost',
            old_name='likes',
            new_name='no_of_likes',
        ),
    ]
