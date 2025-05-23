from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Lesson, Material, Resource, Curriculum

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

class MaterialModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='matuser', password='secret')
    
    def test_material_str(self):
        material = Material.objects.create(
            title="Test Material",
            content="Material content.",
            user=self.user
        )
        self.assertEqual(str(material), "Test Material")
        self.assertEqual(material.user.username, "matuser")

class ResourceModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='resuser', password='pw')
    
    def test_resource_creation(self):
        resource = Resource.objects.create(
            title="Test Resource",
            url="https://example.com",
            user=self.user
        )
        self.assertEqual(str(resource), "Test Resource")
        self.assertEqual(resource.url, "https://example.com")

class CurriculumModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='curruser', password='pw')
    
    def test_curriculum_creation(self):
        curriculum = Curriculum.objects.create(
            title="Test Curriculum",
            user=self.user
        )
        self.assertEqual(str(curriculum), "Test Curriculum")
        self.assertEqual(curriculum.user.username, "curruser")

class LessonViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='viewuser', password='pw')
        self.lesson = Lesson.objects.create(
            title="View Test Lesson",
            description="Lesson description.",
            user=self.user
        )

    def test_lesson_detail_view(self):
        response = self.client.get(f'/lesson/{self.lesson.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "View Test Lesson")