# Generated by Django 2.2.7 on 2019-11-13 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login_Registration', '0002_auto_20191113_1835'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birthday',
            field=models.DateTimeField(null=True),
        ),
    ]
