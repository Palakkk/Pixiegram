# Generated by Django 3.1.2 on 2023-06-16 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0012_userregister_bg_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userregister',
            name='portfolio_img',
            field=models.ImageField(blank=True, default='/media/portfolio_images/default_pro_pic.jpeg', null=True, upload_to='portfolio_images'),
        ),
    ]
