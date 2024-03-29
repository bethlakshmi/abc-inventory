# Generated by Django 3.0.14 on 2021-12-21 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_item_updated_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True,
                                        serialize=False,
                                        verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Performer',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True,
                                        serialize=False,
                                        verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('size_info', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True,
                                        serialize=False,
                                        verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('description', models.TextField(blank=True)),
                ('first_performed', models.DateField(blank=True, null=True)),
                ('last_performed', models.DateField(blank=True, null=True)),
                ('venue_name', models.CharField(blank=True,
                                                max_length=128,
                                                null=True)),
                ('city',
                 models.CharField(blank=True, max_length=128, null=True)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.AddField(
            model_name='item',
            name='last_used',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='item',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='item',
            name='size',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='subitem',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='subitem',
            name='size',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.CreateModel(
            name='Act',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True,
                                        serialize=False,
                                        verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('notes', models.TextField(blank=True)),
                ('first_performed', models.DateField(blank=True, null=True)),
                ('last_performed', models.DateField(blank=True, null=True)),
                ('song', models.CharField(blank=True, max_length=128)),
                ('song_artist', models.CharField(blank=True, max_length=128)),
                ('performers',
                 models.ManyToManyField(max_length=128,
                                        to='inventory.Performer')),
                ('shows', models.ManyToManyField(blank=True,
                                                 max_length=128,
                                                 to='inventory.Show')),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.AddField(
            model_name='item',
            name='acts',
            field=models.ManyToManyField(blank=True,
                                         max_length=128,
                                         to='inventory.Act'),
        ),
        migrations.AddField(
            model_name='item',
            name='colors',
            field=models.ManyToManyField(blank=True,
                                         max_length=128,
                                         to='inventory.Color'),
        ),
        migrations.AddField(
            model_name='item',
            name='performers',
            field=models.ManyToManyField(blank=True,
                                         max_length=128,
                                         to='inventory.Performer'),
        ),
        migrations.AddField(
            model_name='item',
            name='shows',
            field=models.ManyToManyField(blank=True,
                                         max_length=128,
                                         to='inventory.Show'),
        ),
        migrations.AddField(
            model_name='subitem',
            name='performers',
            field=models.ManyToManyField(blank=True,
                                         max_length=128,
                                         to='inventory.Performer'),
        ),
    ]
