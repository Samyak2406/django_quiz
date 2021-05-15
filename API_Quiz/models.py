from django.db import models

# Create your models here.

class Quiz_Details(models.Model):
	quiz_name = models.CharField(max_length = 300)
	quiz_time = models.IntegerField()
	quiz_end = models.IntegerField()
	def __str__(self):
		return self.quiz_name

class Question(models.Model):
	question_text  = models.CharField(max_length = 300)
	correct_ans = models.CharField(max_length = 300)
	quiz = models.ForeignKey(Quiz_Details, related_name = 'Quiz_Set', on_delete = models.CASCADE)
	image = models.ImageField(null = True, blank = True, upload_to = "images/")
	isOpenText = models.BooleanField(blank = True, default = False)
	question_number = models.IntegerField(blank = True)
	def __str__(self):
		return str(self.id)

class Option(models.Model):
	option_text = models.CharField(max_length = 300)
	question = models.ForeignKey(Question, related_name = 'Question_Set', on_delete = models.CASCADE)	

class Submission(models.Model):
	user_id = models.CharField(max_length = 300)
	question_id = models.IntegerField(blank = True)
	quiz_id = models.ForeignKey(Quiz_Details, related_name = 'Quiz_ref_Set', on_delete = models.CASCADE)	
	submission_text = models.CharField(max_length = 1000)
	def __str__(self):
		return str(self.question_id) + " - " +str(self.user_id)



# Answer - in ques -DONE
# Add options - DONE
# Add bool to open text - DONE
# submission optimise - DONE
# Check Score - DONE
# Cover cases in open text - DONE
# quiz 0/1/2 to string - DONE
# requirements.txt - DONE (pip freeze > requirements.txt)
