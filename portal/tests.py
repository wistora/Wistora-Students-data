from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Answer, Question, Quiz, Student


class PortalFlowTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='student', password='strong-pass-123')
		self.student = Student.objects.create(user=self.user, phone_number='555-0001', college_name='WIS College')
		self.quiz = Quiz.objects.create(title='Science', is_published=True)
		self.question = Question.objects.create(
			quiz=self.quiz, text='What is H2O?', option_a='Water', option_b='Oxygen',
			option_c='Hydrogen', option_d='Salt', correct_option='A',
		)

	def test_anonymous_dashboard_redirects(self):
		response = self.client.get(reverse('dashboard'))
		self.assertRedirects(response, f'{reverse("login")}?next={reverse("dashboard")}')

	def test_student_can_log_out_with_post(self):
		self.client.login(username='student', password='strong-pass-123')
		response = self.client.post(reverse('logout'))
		self.assertRedirects(response, reverse('login'))
		self.assertFalse(response.wsgi_request.user.is_authenticated)

	def test_staff_dashboard_redirects_to_login(self):
		User.objects.create_superuser(username='admin', password='strong-pass-123', email='admin@example.com')
		self.client.login(username='admin', password='strong-pass-123')
		response = self.client.get(reverse('dashboard'))
		self.assertRedirects(response, reverse('login'))
		self.assertFalse(response.wsgi_request.user.is_authenticated)

	def test_register_creates_student_and_logs_in(self):
		response = self.client.post(reverse('register'), {
			'username': 'new-student', 'email': 'new@example.com', 'phone_number': '555-0002',
			'college_name': 'New College', 'password': 'strong-pass-123',
		})
		self.assertRedirects(response, reverse('dashboard'))
		self.assertTrue(response.wsgi_request.user.is_authenticated)
		self.assertTrue(Student.objects.filter(phone_number='555-0002').exists())

	def test_student_can_submit_quiz_and_view_result(self):
		self.client.login(username='student', password='strong-pass-123')
		quiz_page = self.client.get(reverse('take_quiz', args=[self.quiz.id]))
		self.assertContains(quiz_page, 'What is H2O?')
		response = self.client.post(reverse('take_quiz', args=[self.quiz.id]), {f'question_{self.question.id}': 'A'})
		self.assertEqual(response.status_code, 302)
		self.assertEqual(Answer.objects.get().is_correct, True)
		self.assertContains(self.client.get(response.url), '1/1')

	def test_student_dashboard_lists_published_quiz_and_links_to_exam(self):
		self.client.login(username='student', password='strong-pass-123')
		response = self.client.get(reverse('dashboard'))

		self.assertContains(response, self.quiz.title)
		self.assertContains(response, reverse('take_quiz', args=[self.quiz.id]))

		self.quiz.is_published = False
		self.quiz.save(update_fields=['is_published'])
		response = self.client.get(reverse('dashboard'))
		self.assertNotContains(response, self.quiz.title)
