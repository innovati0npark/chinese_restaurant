# Generated by Django 5.0.4 on 2024-04-17 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='description',
            field=models.TextField(),
        ),
    ]
