# Generated by Django 3.2 on 2024-03-01 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_role_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='role',
        ),
        migrations.AddField(
            model_name='myuser',
            name='role',
            field=models.CharField(blank=True, max_length=256, verbose_name='role'),
        ),
        migrations.DeleteModel(
            name='Role',
        ),
    ]
