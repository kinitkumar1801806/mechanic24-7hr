# Generated by Django 3.0.4 on 2020-04-22 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='mechanic_i',
            field=models.CharField(default='', max_length=100),
        ),
    ]
