# Generated by Django 4.2.4 on 2023-11-06 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("achats", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Category",
            new_name="Categorie",
        ),
        migrations.RenameField(
            model_name="achat",
            old_name="category",
            new_name="categorie",
        ),
        migrations.RenameField(
            model_name="categorie",
            old_name="nomCategory",
            new_name="nomCategorie",
        ),
    ]
