# Generated by Django 3.2.8 on 2022-05-13 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student_app', '0004_alter_scores_score'),
    ]

    operations = [
        migrations.RenameField(
            model_name='term',
            old_name='slug',
            new_name='term_slug',
        ),
    ]