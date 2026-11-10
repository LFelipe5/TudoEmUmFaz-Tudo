from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Task
from .scraper import validate_url


class ToolboxTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user('owner', password='test-password')
        self.other = get_user_model().objects.create_user('other', password='test-password')

    def test_tools_require_login(self):
        for name in ['home', 'tasks', 'scraper']:
            self.assertEqual(self.client.get(reverse(name)).status_code, 302)

    def test_task_lifecycle_and_ownership(self):
        self.client.force_login(self.user)
        self.client.post(reverse('tasks'), {'title': 'Build toolbox'})
        task = Task.objects.get()
        self.assertEqual(task.owner, self.user)
        self.client.post(reverse('task-action', args=[task.pk, 'toggle']))
        task.refresh_from_db()
        self.assertTrue(task.completed)
        self.client.force_login(self.other)
        self.assertNotContains(self.client.get(reverse('tasks')), task.title)
        for action in ['toggle', 'delete']:
            self.assertEqual(self.client.post(reverse('task-action', args=[task.pk, action])).status_code, 404)
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(reverse('task-action', args=[task.pk, 'delete'])).status_code, 405)
        self.client.post(reverse('task-action', args=[task.pk, 'delete']))
        self.assertFalse(Task.objects.exists())

    def test_templates_render(self):
        self.assertEqual(self.client.get(reverse('login')).status_code, 200)
        self.client.force_login(self.user)
        for name in ['home', 'tasks', 'scraper']:
            self.assertEqual(self.client.get(reverse(name)).status_code, 200)

    @patch('core.views.scrape', return_value={'title': '<script>bad</script>', 'url': 'https://example.com', 'headings': ['Example'], 'links': []})
    def test_scraper_renders_escaped_output(self, fetch):
        self.client.force_login(self.user)
        response = self.client.post(reverse('scraper'), {'url': 'https://example.com'})
        self.assertContains(response, '&lt;script&gt;bad&lt;/script&gt;')
        self.assertNotContains(response, '<script>bad</script>')

    def test_scraper_rejects_private_destinations(self):
        with patch('core.scraper.socket.getaddrinfo', return_value=[(2, 1, 6, '', ('127.0.0.1', 80))]):
            with self.assertRaises(ValueError):
                validate_url('http://localhost/')
        for url in ['file:///etc/passwd', 'http://user:pass@example.com', 'https://example.com:8443']:
            with self.assertRaises(ValueError):
                validate_url(url)
