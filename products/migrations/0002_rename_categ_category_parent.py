# Generated by Django 4.0.5 on 2022-07-12 05:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='categ',
            new_name='parent',
        ),
    ]
