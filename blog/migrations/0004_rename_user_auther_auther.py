# Generated by Django 4.2.2 on 2023-09-15 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auther_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auther',
            old_name='user',
            new_name='auther',
        ),
    ]