# Generated by Django 2.1.4 on 2022-11-28 01:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_auto_20221128_0040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.BinaryField(null=True),
        ),
        migrations.AlterField(
            model_name='thread',
            name='closed_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin_user', to='forum.CustomUser'),
        ),
    ]
