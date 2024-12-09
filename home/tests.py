from django.test import RequestFactory, TestCase
from myapp.views import HomePageView

class HomePageViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_home_page_status_code(self):
        request = self.factory.get('/')
        response = HomePageView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_home_page_content(self):
        request = self.factory.get('/')
        response = HomePageView.as_view()(request)
        self.assertContains(response, "Welcome to my website!")

