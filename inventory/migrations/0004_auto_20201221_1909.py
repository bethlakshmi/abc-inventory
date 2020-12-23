# Generated by Django 2.2.17 on 2020-12-21 19:09

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_usermessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='StyleProperty',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True,
                                        serialize=False,
                                        verbose_name='ID')),
                ('style_property', models.CharField(max_length=300)),
                ('value_type', models.CharField(
                    choices=[('color', 'color')],
                    default='color',
                    max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'style properties',
                'ordering': ['selector', 'style_property'],
            },
        ),
        migrations.CreateModel(
            name='StyleSelector',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True,
                                        serialize=False,
                                        verbose_name='ID')),
                ('selector', models.CharField(max_length=300)),
                ('description', models.TextField(blank=True)),
                ('pseudo_class', models.CharField(blank=True,
                                                  max_length=128,
                                                  null=True)),
                ('target_element_usage', models.CharField(max_length=100)),
                ('used_for', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['selector', 'pseudo_class'],
            },
        ),
        migrations.CreateModel(
            name='StyleVersion',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True,
                                        serialize=False,
                                        verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('number', models.DecimalField(
                    decimal_places=3,
                    max_digits=12,
                    validators=[django.core.validators.MinValueValidator(
                        Decimal('0.00'))])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('currently_live', models.BooleanField(default=False)),
                ('currently_test', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['name', 'number'],
                'unique_together': {('name', 'number')},
            },
        ),
        migrations.CreateModel(
            name='StyleValue',
            fields=[
                ('id', models.AutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID')),
                ('value', models.CharField(max_length=200)),
                ('style_property', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='inventory.StyleProperty')),
                ('style_version', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='inventory.StyleVersion')),
            ],
            options={
                'ordering': ['style_version', 'style_property'],
            },
        ),
        migrations.AddConstraint(
            model_name='styleselector',
            constraint=models.UniqueConstraint(
                fields=('selector', 'pseudo_class'),
                name='unique_selector'),
        ),
        migrations.AddField(
            model_name='styleproperty',
            name='selector',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='inventory.StyleSelector'),
        ),
        migrations.AddConstraint(
            model_name='stylevalue',
            constraint=models.UniqueConstraint(
                fields=('style_property', 'style_version'),
                name='unique_value'),
        ),
        migrations.AddConstraint(
            model_name='styleproperty',
            constraint=models.UniqueConstraint(
                fields=('selector', 'style_property'),
                name='unique_property'),
        ),
    ]
