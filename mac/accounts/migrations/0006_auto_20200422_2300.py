# Generated by Django 3.0.4 on 2020-04-22 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_contact_mechanic_i'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='mechanic_i',
            new_name='mechanic_id',
        ),
    ]