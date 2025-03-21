# Generated by Django 5.1.7 on 2025-03-14 22:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer_app', '0005_fileupload_alter_offer_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='image',
            field=models.FileField(null=True, upload_to='uploads/'),
        ),
        migrations.AlterField(
            model_name='offerdetail',
            name='offer',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='details', to='offer_app.offer'),
        ),
        migrations.AlterField(
            model_name='offerdetail',
            name='revisions',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='offerdetail',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
