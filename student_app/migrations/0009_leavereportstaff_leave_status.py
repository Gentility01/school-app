# Generated by Django 3.2.8 on 2022-05-17 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_app', '0008_rename_class_id_student_s_class'),
    ]

    operations = [
        migrations.AddField(
            model_name='leavereportstaff',
            name='leave_status',
            field=models.IntegerField(default=0),
        ),
    ]
