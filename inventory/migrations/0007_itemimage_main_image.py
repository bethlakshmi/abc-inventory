# Generated by Django 2.2.19 on 2021-03-23 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_auto_20210216_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemimage',
            name='main_image',
            field=models.BooleanField(default=False),
        ),
    ]