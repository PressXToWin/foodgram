# Generated by Django 4.2.2 on 2023-07-07 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0012_alter_favorite_options_alter_shoppingcart_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredient',
            name='amount',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество'),
        ),
    ]
