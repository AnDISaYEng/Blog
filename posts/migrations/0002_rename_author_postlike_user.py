# Generated by Django 4.0 on 2021-12-26 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postlike',
            old_name='author',
            new_name='user',
        ),
    ]