# Generated by Django 3.2.9 on 2021-11-15 08:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20211115_0825'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='uuid',
            new_name='id',
        ),
    ]
