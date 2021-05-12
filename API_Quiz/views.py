from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import *
from rest_framework.authentication import *
from time import time
import math

# Create your views here.

class get_all_quiz(APIView):

	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request, id = None):
		if id == None or (id>2 or id<0):
			quizzes = Quiz_Details.objects.all()
			serializer = quiz_serializer(quizzes, many = True)
			return Response(serializer.data)
		else:
			
			cur_time = time()
			cur_time = math.ceil(cur_time)

			if id == 0:
				quizzes = Quiz_Details.objects.filter(quiz_end__lt = cur_time)
				serializer = quiz_serializer(quizzes, many = True)
				return Response(serializer.data)
			elif id == 1:
				quizzes = Quiz_Details.objects.filter(quiz_time__lte = cur_time).filter(quiz_end__gte = cur_time)
				serializer = quiz_serializer(quizzes, many = True)
				return Response(serializer.data)
			else:
				quizzes = Quiz_Details.objects.filter(quiz_time__gt = cur_time)
				serializer = quiz_serializer(quizzes, many = True)
				return Response(serializer.data)


class attend_quiz(APIView):

	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	def post(self, request, id):
		cur_time = time()
		cur_time = (math.ceil(cur_time))
		quiz = Quiz_Details.objects.filter(id = id)
		if len(quiz)<=0:
			return Response("Invalid Request")
		quiz = quiz[0]
		request.data['quiz_id'] = id
		request.data['user_id'] = request.user.username

		if 'submission_text' in request.data:
			ls = request.data['submission_text']
			request.data['submission_text'] = "___".join(str(x) for x in ls) # I have used ___ as separator for answers
			print(request.data)
		if cur_time >= (quiz.quiz_time) and cur_time <= (quiz.quiz_end):
			if request.user.username not in quiz.submission:
				serializer = submission_serializer(data = (request.data))
				if serializer.is_valid() == False:
					return Response("Invalid Data")
				serializer.save()
				quiz.submission+= " "+str(request.user.username)
				quiz.save()
				return Response("submission successful")
			else:
				return Response("You can submit only once")
		else:
			return Response("Quiz is not currently Active")



class question_paper(APIView):
	
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated, IsAdminUser]

	def post(self, request):

		def checkQuiz(data):
			serializer = quiz_serializer(data = data)
			if serializer.is_valid():
				return True
			return serializer.errors

		def checkPairs(data):

			if len(data)<1:
				return "Please enter Questions"

			for ques in data:

				if len(list(ques.keys())) in [3, 4]:
					for key in list(ques.keys()):

						if (key == 'question_text' or key == 'options') or (key == 'correct_ans' or key == 'image'):
							continue
						return 'Invalid keys'
				else:
					return 'Invalid keys'

				if len(ques['question_text']) < 1:
					return "Please enter Valid Question"
				
				
				options = len(ques['options'])
				ans = ques['correct_ans']
				print(options)

				if (((options<5 and options%2==0)) and (ans in ques['options'])) or options == 0:
					continue
				else:
					return "Enter valid options and answer"
			return True
			
		# Go ON
		quizBool = checkQuiz(request.data['quiz'])
		quizQues = checkPairs(request.data['pairs'])
		if quizBool != True:
			return Response(quizBool)
		if quizQues != True:
			return Response(quizQues)

		# All the fields are valid

		serializer = quiz_serializer(data = request.data['quiz'])
		if serializer.is_valid():
			back = serializer.save()
			roll_back_serializer = back
			bid = back.id

			for ques in request.data['pairs']:
				ques['quiz'] = bid
				serializer = question_serializer(data = ques)
				if serializer.is_valid():
					sback = serializer.save()
					sid = sback.id
					for ans in ques['options']:
						dic = {}
						dic['answer_text'] = ans
						dic['question'] = sid
						new_serializer = answer_serializer(data = dic)
					
						if new_serializer.is_valid():
							instance = new_serializer.save()
						else:
							Response(new_serializer.errors)
					
				else:
					roll_back_serializer.delete()
					Response("Unknown Error")
			return Response("All THe Data has been saved")
		else:
			roll_back_serializer.delete()
			Response("Unknown Error")
