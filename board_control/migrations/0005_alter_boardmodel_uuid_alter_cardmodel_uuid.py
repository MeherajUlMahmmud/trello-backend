# Generated by Django 5.0 on 2024-09-20 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board_control', '0004_boardmodel_uuid_cardmodel_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boardmodel',
            name='uuid',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='cardmodel',
            name='uuid',
            field=models.CharField(default='UUID', max_length=255, unique=True),
            preserve_default=False,
        ),
    ]
