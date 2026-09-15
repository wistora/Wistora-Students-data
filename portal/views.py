from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .models import Answer, Attempt, Quiz, Student


def register(request):
	if request.user.is_authenticated:
		return redirect('dashboard')
	if request.method == 'POST':
		username = request.POST.get('username', '').strip()
		email = request.POST.get('email', '').strip()
		password = request.POST.get('password', '')
		phone_number = request.POST.get('phone_number', '').strip()
		college_name = request.POST.get('college_name', '').strip()
		if not all([username, email, password, phone_number]):
			messages.error(request, 'Please complete all required fields.')
		elif User.objects.filter(username=username).exists() or Student.objects.filter(phone_number=phone_number).exists():
			messages.error(request, 'That username or phone number is already in use.')
		else:
			user = User.objects.create_user(username=username, email=email, password=password)
			Student.objects.create(user=user, phone_number=phone_number, college_name=college_name)
			login(request, user)
			return redirect('dashboard')
	return render(request, 'portal/register.html')


def login_view(request):
	if request.user.is_authenticated:
		return redirect('dashboard')
	form = AuthenticationForm(request, data=request.POST or None)
	if request.method == 'POST' and form.is_valid():
		login(request, form.get_user())
		return redirect('dashboard')
	return render(request, 'portal/login.html', {'form': form})


@login_required
def dashboard(request):
	try:
		student = request.user.student_profile
	except Student.DoesNotExist:
		logout(request)
		messages.error(request, 'Your account is not linked to a student profile.')
		return redirect('login')
	quizzes = Quiz.objects.filter(is_published=True).prefetch_related('questions')
	attempts = student.attempts.select_related('quiz')[:5]
	return render(request, 'portal/dashboard.html', {'quizzes': quizzes, 'attempts': attempts})


@login_required
def take_quiz(request, quiz_id):
	quiz = get_object_or_404(Quiz.objects.prefetch_related('questions'), pk=quiz_id, is_published=True)
	questions = list(quiz.questions.all())
	if request.method == 'POST':
		with transaction.atomic():
			attempt = Attempt.objects.create(student=request.user.student_profile, quiz=quiz)
			score = 0
			for question in questions:
				selected = request.POST.get(f'question_{question.id}', '')
				is_correct = selected == question.correct_option
				score += int(is_correct)
				Answer.objects.create(attempt=attempt, question=question, selected_option=selected, is_correct=is_correct)
			attempt.score = score
			attempt.save(update_fields=['score'])
		return redirect('result', attempt_id=attempt.id)
	return render(request, 'portal/take_quiz.html', {'quiz': quiz, 'questions': questions})


@login_required
def result(request, attempt_id):
	attempt = get_object_or_404(Attempt.objects.select_related('quiz'), pk=attempt_id, student=request.user.student_profile)
	total_questions = attempt.total_questions
	score_percent = round((attempt.score / total_questions) * 100) if total_questions else 0
	return render(request, 'portal/result.html', {
		'attempt': attempt,
		'score_percent': score_percent,
	})


@login_required
def history(request):
	attempts = request.user.student_profile.attempts.select_related('quiz').prefetch_related('answers')
	return render(request, 'portal/history.html', {'attempts': attempts})
