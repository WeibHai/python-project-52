# Generated by Django 4.2.1 on 2023-06-10 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statuses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statuses',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Status name'),
        ),
    ]
