# Generated by Django 5.1.2 on 2024-12-18 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_alter_assembly_product_alter_component_assembly_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assembly',
            name='product',
        ),
        migrations.RemoveField(
            model_name='component',
            name='assembly',
        ),
    ]