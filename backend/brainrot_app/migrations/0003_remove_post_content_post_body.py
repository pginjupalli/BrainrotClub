# Generated by Django 5.1.6 on 2025-02-22 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brainrot_app', '0002_remove_post_id_post_uuid_alter_video_uuid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='content',
        ),
        migrations.AddField(
            model_name='post',
            name='body',
            field=models.TextField(blank=True, null=True),
        ),
    ]
