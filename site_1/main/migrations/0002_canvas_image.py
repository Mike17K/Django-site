# Generated by Django 4.1 on 2022-09-06 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='canvas',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
