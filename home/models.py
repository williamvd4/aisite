from django.db import models
from django.contrib.auth.models import User


class MyFormModel(models.Model):
    Title = models.TextField(max_length=100)
    Grade = [
        ("prek", "PreK"),
        ("kindergarten", "Kindergarten"),
        ("1st", "1st"),
        ("2nd", "2nd"),
        ("3rd", "3rd"),
        ("4th", "4th"),
        ("5th", "5th"),
        ("6th", "6th"),
        ("7th", "7th"),
        ("8th", "8th"),
        ("9th", "9th"),
        ("10th", "10th"),
        ("11th", "11th"),
        ("12th", "12th"),
    ]
    grade = models.CharField(max_length=255, choices=Grade)

    Subject = [
        ("Math", "Math"),
        ("Science", "Science"),
        ("Social Studies", "Social Studies"),
        ("Language Arts", "Language Arts"),
        ("Art", "Art"),
        ("Music", "Music"),
        ("Physical Education", "Physical Education"),
        ("Health", "Health"),
        ("Technology", "Technology"),
        ("World Language", "World Language"),
        ("Other", "Other"),
    ]
    subject = models.CharField(max_length=255, choices=Subject)

    Aim = models.TextField(max_length=255)

    Objectives = models.TextField(max_length=255)
    Materials = models.TextField(max_length=255)
    Procedure = models.TextField(max_length=255)
    Assessment = models.TextField(max_length=255)
    Differentiation = models.TextField(max_length=255)

    class Meta:
        verbose_name = "My Form"
        verbose_name_plural = "My Forms"
        ordering = ["grade"]

    def __str__(self):
        return "My Form Instance"

    objects = models.Manager()


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lessons")

    def __str__(self):
        return self.title


class Material(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="materials")

    def __str__(self):
        return self.title


class Resource(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="resources")

    def __str__(self):
        return self.title


class Curriculum(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="curriculums/", null=True)

    def __str__(self):
        return self.title
