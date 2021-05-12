from django.db import models

# Create your models here.

class Quiz_Details(models.Model):
	quiz_name = models.CharField(max_length = 300)
	quiz_time = models.IntegerField()
	quiz_end = models.IntegerField()
	submission = models.CharField(max_length = 100000, blank = True)
	def __str__(self):
		return self.quiz_name


class Question(models.Model):
	question_text  = models.CharField(max_length = 300)
	correct_ans = models.CharField(max_length = 300)
	quiz = models.ForeignKey(Quiz_Details, related_name = 'Quiz_Set', on_delete = models.CASCADE)
	image = models.ImageField(null = True, blank = True, upload_to = "images/")
	def __str__(self):
		return str(self.id)

class Answer(models.Model):
	answer_text = models.CharField(max_length = 300)
	question = models.ForeignKey(Question, related_name = 'Question_Set', on_delete = models.CASCADE)	

class Submission(models.Model):
	user_id = models.CharField(max_length = 300)
	quiz_id = models.ForeignKey(Quiz_Details, related_name = 'Submission_Set', on_delete = models.CASCADE)
	submission_text = models.CharField(max_length = 1000)
	def __str__(self):
		return str(self.quiz_id) + " - " +str(self.user_id)
