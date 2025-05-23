from django.test import TestCase
from django.contrib.auth.models import User
from .models import Lesson

class LessonModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_lesson_creation(self):
        lesson = Lesson.objects.create(
            title="Test Lesson",
            description="A test description.",
            user=self.user
        )
        self.assertEqual(lesson.title, "Test Lesson")
        self.assertEqual(lesson.user.username, "testuser")