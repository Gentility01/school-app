# Generated by Django 3.2.8 on 2022-05-13 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_app', '0005_rename_slug_term_term_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='term_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='student_app.term'),
        ),
    ]