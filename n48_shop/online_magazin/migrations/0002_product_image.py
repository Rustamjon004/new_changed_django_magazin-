# Generated by Django 5.0.7 on 2024-08-01 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_magazin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='products'),
        ),
    ]
