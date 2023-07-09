# Generated by Django 3.1.2 on 2023-06-16 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0015_auto_20230616_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userregister',
            name='bg_img',
            field=models.ImageField(default='default_bg_img.jpg', upload_to='bg_images'),
        ),
        migrations.AlterField(
            model_name='userregister',
            name='portfolio_img',
            field=models.ImageField(default='default_pro_pic.jpeg', upload_to='portfolio_images'),
        ),
    ]
