# Generated by Django 4.1.4 on 2023-05-10 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contatcus',
            old_name='user_name',
            new_name='name',
        ),
    ]
