import os

import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')
if not settings.configured:
    django.setup()

import csv
import logging

from django.db import IntegrityError
from reviews.models import Title, Category, Genre, GenreTitle, Comment, Review
from user.models import MyUser


def import_data_from_csv(file_path, model):
    DEBUG_MESSAGE = f'path: {file_path}, model: {model}'
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        columns = reader.fieldnames
        logging.debug('Началась загрузка csv файла\n' + DEBUG_MESSAGE)
        for row in reader:
            data = {}
            for column in columns:
                if column == 'category':
                    category_id = int(row[column])
                    data[column] = Category.objects.get(id=category_id)
                elif column == 'author':
                    user_id = int(row[column])
                    data[column] = MyUser.objects.get(id=user_id)
                else:
                    data[column] = row[column]
            try:
                model.objects.create(**data)
            except IntegrityError:
                pass
        logging.debug('Завершилась загрузка csv файла\n' + DEBUG_MESSAGE)


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
