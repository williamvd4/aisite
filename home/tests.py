from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import LessonPlan, Material, Resource, Curriculum, Subject, Grade

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
        self.subject = Subject.objects.create(name='Math')
        self.grade = Grade.objects.create(level='5th', order=5)
        self.lesson_plan = LessonPlan.objects.create(
            title="View Test Lesson",
            description="Lesson description.",
            subject=self.subject,
            grade=self.grade,
            learning_objectives='Learn fractions',
            materials_needed='Whiteboard',
            opening_activity='Warm-up',
            main_instruction='Direct instruction',
            closing_activity='Exit ticket',
            formative_assessment='Q&A',
            differentiation_strategies='Small groups',
            user=self.user,
        )

    def test_lesson_detail_view(self):
        self.client.login(username='viewuser', password='pw')
        response = self.client.get(reverse('home:lesson_detail', args=[self.lesson_plan.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "View Test Lesson")
