# Generated by Django 2.2.15 on 2022-12-02 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0008_auto_20221129_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]