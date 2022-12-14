# Generated by Django 2.1.4 on 2022-11-27 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='thread',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='forum.Thread'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='thread',
            name='section',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='forum.Section'),
            preserve_default=False,
        ),
    ]
