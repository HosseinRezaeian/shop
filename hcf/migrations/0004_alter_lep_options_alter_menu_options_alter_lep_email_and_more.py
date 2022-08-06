# Generated by Django 4.0.6 on 2022-08-02 06:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hcf', '0003_lep'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lep',
            options={'verbose_name': '', 'verbose_name_plural': 'لوگو ایمیل تلفن'},
        ),
        migrations.AlterModelOptions(
            name='menu',
            options={'verbose_name': 'منو ', 'verbose_name_plural': 'منو'},
        ),
        migrations.AlterField(
            model_name='lep',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='ایمیل'),
        ),
        migrations.AlterField(
            model_name='lep',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='image', verbose_name='لوگو'),
        ),
        migrations.AlterField(
            model_name='lep',
            name='phone',
            field=models.IntegerField(blank=True, null=True, verbose_name='تلفن'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='sub_menu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hcf.menu', verbose_name='زیر منو'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='title',
            field=models.CharField(max_length=30, verbose_name='عنوان'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='url_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='لینک'),
        ),
    ]