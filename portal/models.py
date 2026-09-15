from django.contrib.auth.models import User
from django.db import models


class Student(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
	phone_number = models.CharField(max_length=20, unique=True)
	college_name = models.CharField(max_length=150, blank=True)
	joined_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.phone_number} - {self.user.get_full_name() or self.user.username}'


class Quiz(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	is_published = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return self.title


class Question(models.Model):
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
	text = models.TextField()
	option_a = models.CharField(max_length=300)
	option_b = models.CharField(max_length=300)
	option_c = models.CharField(max_length=300)
	option_d = models.CharField(max_length=300)
	correct_option = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
	order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ['order', 'id']

	def __str__(self):
		return f'{self.quiz}: {self.text[:60]}'


class Attempt(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attempts')
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
	score = models.PositiveIntegerField(default=0)
	completed_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-completed_at']

	@property
	def total_questions(self):
		return self.quiz.questions.count()

	def __str__(self):
		return f'{self.student} - {self.quiz} ({self.score}/{self.total_questions})'


class Answer(models.Model):
	attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE, related_name='answers')
	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
	selected_option = models.CharField(max_length=1, blank=True)
	is_correct = models.BooleanField(default=False)

	class Meta:
		constraints = [models.UniqueConstraint(fields=['attempt', 'question'], name='unique_attempt_question')]

	def __str__(self):
		return f'{self.attempt} - {self.question}'
