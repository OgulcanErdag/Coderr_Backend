# Generated by Django 5.1.7 on 2025-03-15 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication_app', '0004_alter_fileupload_file'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FileUpload',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='image',
            field=models.FileField(null=True, upload_to='profile_pics/'),
        ),
    ]
