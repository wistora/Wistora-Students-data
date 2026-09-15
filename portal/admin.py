from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Answer, Attempt, Question, Quiz, Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
	list_display = ('phone_number', 'user', 'college_name', 'joined_at')
	search_fields = ('phone_number', 'college_name', 'user__username', 'user__email', 'user__first_name', 'user__last_name')
	list_filter = ('college_name',)


class QuestionInline(admin.TabularInline):
	model = Question
	extra = 1


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
	list_display = ('title', 'is_published', 'question_count', 'created_at')
	list_filter = ('is_published',)
	search_fields = ('title', 'description')
	inlines = [QuestionInline]
	fieldsets = (
		(None, {'fields': ('title', 'description')}),
		('Student visibility', {
			'fields': ('is_published',),
			'description': 'Only published quizzes appear on the student dashboard and can be attempted.',
		}),
	)

	@admin.display(description='Questions')
	def question_count(self, obj):
		return obj.questions.count()


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
	list_display = ('student', 'quiz', 'score', 'completed_at')
	list_filter = ('quiz',)
	search_fields = ('student__phone_number', 'student__user__username', 'quiz__title')
	readonly_fields = ('completed_at',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
	list_display = ('attempt', 'question', 'selected_option', 'is_correct')
	list_filter = ('is_correct',)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register your models here.
