# Generated by Django 2.1.4 on 2018-12-20 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmpInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('age', models.IntegerField(default=0)),
                ('birth', models.DateField()),
                ('hiredate', models.DateTimeField()),
                ('recordtime', models.TimeField()),
                ('hirdstatus', models.BooleanField()),
                ('photo', models.ImageField(upload_to='media/img/')),
                ('mail', models.EmailField(max_length=254)),
                ('salary', models.DecimalField(decimal_places=2, max_digits=7)),
                ('attachments', models.FileField(upload_to='media/file/')),
            ],
        ),
    ]
