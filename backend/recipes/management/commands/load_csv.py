from csv import reader

from django.core.management import BaseCommand

from recipes.models import Ingredient

from django.db.utils import IntegrityError


class Command(BaseCommand):

    def handle(self, *args, **options):
        print(f'Loading ingredients data')
        for row in reader(
                open('../data/ingredients.csv', encoding="utf8")):
            ingredient = Ingredient(
                name=row[0],
                measurement_unit=row[1]
            )
            try:
                ingredient.save()
            except IntegrityError as err:
                print(err)
