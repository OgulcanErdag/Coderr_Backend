# Generated by Django 5.1.7 on 2025-03-15 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer_app', '0008_alter_offer_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='image',
            field=models.FileField(null=True, upload_to='offer_pics/'),
        ),
    ]
