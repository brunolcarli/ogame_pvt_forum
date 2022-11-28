# Generated by Django 2.1.4 on 2022-11-28 01:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0006_thread_last_post_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posted_by', to='forum.CustomUser'),
        ),
    ]
