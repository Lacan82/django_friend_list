# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-25 14:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('alias', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('don', models.DateField()),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='friend',
            name='current_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Owner', to='friends.User'),
        ),
        migrations.AddField(
            model_name='friend',
            name='friends',
            field=models.ManyToManyField(to='friends.User'),
        ),
    ]
