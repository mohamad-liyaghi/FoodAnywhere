# Generated by Django 5.0.7 on 2024-08-05 10:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0002_alter_product_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="is_deleted",
            field=models.BooleanField(default=False),
        ),
    ]