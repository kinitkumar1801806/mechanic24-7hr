# Generated by Django 3.0.4 on 2020-04-12 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mechanic_accounts',
            name='timeperiod',
            field=models.CharField(default='1 year', max_length=100),
        ),
        migrations.AddField(
            model_name='mechanic_accounts',
            name='totalcustomer',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='mechanic_accounts',
            name='totalsatisfiedcustomer',
            field=models.IntegerField(default=0),
        ),
    ]
