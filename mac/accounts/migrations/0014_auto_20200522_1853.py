# Generated by Django 3.0.4 on 2020-05-22 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20200522_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_accounts',
            name='image',
            field=models.ImageField(default=' ', upload_to='shop/images/'),
        ),
    ]
