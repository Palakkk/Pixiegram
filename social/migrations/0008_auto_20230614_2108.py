# Generated by Django 3.1.2 on 2023-06-14 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0007_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='post',
            new_name='post_user',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='parent_comment',
        ),
    ]
