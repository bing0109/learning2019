# Generated by Django 2.1.4 on 2018-12-19 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django03_login_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=256),
        ),
    ]
