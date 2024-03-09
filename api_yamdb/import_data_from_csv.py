import csv
import os

import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')
if not settings.configured:
    django.setup()

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from user.models import MyUser


def import_data_from_csv(file_path, model):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        columns = reader.fieldnames
        for row in reader:
            data = {}
            for column in columns:
                data[column] = row[column]
            model.objects.create(**data)


paths_models = [
    # Не менять порядок!!!
    ('static/data/users.csv', MyUser),
    ('static/data/genre.csv', Genre),
    ('static/data/category.csv', Category),
    ('static/data/titles.csv', Title),
    ('static/data/genre_title.csv', GenreTitle),
    ('static/data/review.csv', Review),
    ('static/data/comments.csv', Comment),
]


def main():
    for path, model in paths_models:
        import_data_from_csv(path, model)


if __name__ == '__main__':
    main()
