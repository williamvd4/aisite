# Generated by Django 4.2.9 on 2025-05-23 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0006_populate_initial_data"),
    ]

    operations = [
        migrations.AddField(
            model_name="lessonplan",
            name="lesson_date",
            field=models.DateField(
                blank=True, null=True, verbose_name="Date of Lesson"
            ),
        ),
    ]
