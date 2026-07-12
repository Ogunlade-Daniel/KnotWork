from django.test import TestCase
from django.urls import reverse

from .models import Course, Mentor, Review


class HomePageTests(TestCase):
    def test_home_page_displays_featured_learning_content(self):
        Course.objects.create(
            title="AI for Everyone",
            description="A practical introduction to AI for modern teams.",
            duration="6 weeks",
            level="Beginner",
            featured=True,
        )
        Mentor.objects.create(
            name="Amina Okafor",
            title="AI Learning Strategist",
            bio="Amina mentors global learners in launching sustainable study circles.",
            expertise="Artificial Intelligence",
        )
        Review.objects.create(
            name="Liam Chen",
            role="Student",
            testimonial="The live practice rooms helped me build real confidence.",
            rating=5,
            approved=True,
        )

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "AI for Everyone")
        self.assertContains(response, "Amina Okafor")
        self.assertContains(response, "Liam Chen")
