# Generated by Django 4.2.2 on 2023-06-28 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_favorite_unique_favorite_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='text',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=8, unique=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
