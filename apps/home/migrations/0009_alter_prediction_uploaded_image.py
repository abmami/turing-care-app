# Generated by Django 3.2.11 on 2022-05-06 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20220506_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prediction',
            name='uploaded_image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
