import logging
import os
import csv

import django
from django.conf import settings
from django.db import IntegrityError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')
if not settings.configured:
    django.setup()


def import_data_from_csv(file_path, model):
    from user.models import MyUser
    from reviews.models import Category

    debug_message = f'path: {file_path}, model: {model}'

    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        columns = reader.fieldnames
        logging.debug('Началась загрузка csv файла\n' + debug_message)
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
        logging.debug('Завершилась загрузка csv файла\n' + debug_message)


def main():
    from user.models import MyUser
    from reviews.models import (
        Title, Category, Genre, GenreTitle, Comment, Review
    )

    default_path = 'static/data/'
    file_names_models = [
        ('users.csv', MyUser),
        ('genre.csv', Genre),
        ('category.csv', Category),
        ('titles.csv', Title),
        ('genre_title.csv', GenreTitle),
        ('review.csv', Review),
        ('comments.csv', Comment),
    ]

    for file_name, model in file_names_models:
        full_path = os.path.join(default_path, file_name)
        import_data_from_csv(full_path, model)


if __name__ == '__main__':
    main()
