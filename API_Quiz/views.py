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

		# print(id)
		if id == None or (id not in ["live", "past", "future"]):
			quizzes = Quiz_Details.objects.all()
			serializer = quiz_serializer(quizzes, many = True)
			return Response(serializer.data)
		else:
			
			cur_time = time()
			cur_time = math.ceil(cur_time)

			if id == "past":
				quizzes = Quiz_Details.objects.filter(quiz_end__lt = cur_time)
				serializer = quiz_serializer(quizzes, many = True)
				return Response(serializer.data)
			elif id == "live":
				quizzes = Quiz_Details.objects.filter(quiz_time__lte = cur_time).filter(quiz_end__gte = cur_time)
				serializer = quiz_serializer(quizzes, many = True)
				return Response(serializer.data)
			else:
				quizzes = Quiz_Details.objects.filter(quiz_time__gt = cur_time)
				serializer = quiz_serializer(quizzes, many = True)
				return Response(serializer.data)
# map[index] = [3, 2, 1]

class attend_quiz(APIView):

	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	def post(self, request, id):
		cur_time = time()
		cur_time = (math.ceil(cur_time))

		quiz = Quiz_Details.objects.filter(id = id)
		if len(quiz)<=0:
			return Response("Invalid Request")
		
		request.data['user_id'] = request.user.username
		request.data['quiz_id'] = id
		marks = 0

		quiz = quiz[0]
		if (cur_time >= (quiz.quiz_time) and cur_time <= (quiz.quiz_end)) == False:
			return Response("QUiz is not open")
		
		check = Submission.objects.filter(user_id = request.user.username).filter(quiz_id = id)
		if len(check)>=1:
			return Response("You have already submitted")


		if 'submission_text' in request.data:
			ls = request.data['submission_text']
			total_ques = len(Question.objects.filter(quiz = id))

			# CHeck total questions in quiz
			if total_ques!=len(ls):
				return Response("Invalid input")


			for index in range(len(ls)):

				request.data['question_id'] = index
				request.data['submission_text'] = ls[index]
				serializer = submission_serializer(data = request.data)
				if serializer.is_valid():
					serializer.save()
				else:
					return Response(serializer.errors)

				ans_object = Question.objects.filter(quiz = id).filter(question_number = index)
				if (len(ans_object)!=1):
					return Response("Invalid answers")
				ans_object = question_serializer(ans_object[0])
				# print(ans_object['isOpenText'])
				if ans_object.data['isOpenText'] != True:
					if ans_object.data['correct_ans'] == ls[index]:
						marks += 1

				else:

					def checkVariety(a):
						return ''.join(ch.lower() for ch in a if not ch.isspace())
					print(checkVariety(ans_object.data['correct_ans']), checkVariety(ls[index]))
					if checkVariety(ans_object.data['correct_ans']) == checkVariety(ls[index]):
						marks += 1

				# 	Check variety
			return Response("Your Score is: " + str(marks))
		else:
			return Response("Invalid input")



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
				# print(options)

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
			index = -1
			for ques in request.data['pairs']:
				index += 1
				ques['quiz'] = bid
				nos = len(ques['options'])
				if nos!=0:
					ques['isOpenText'] = False
				else:
					ques['isOpenText'] = True
				ques['question_number'] = index
				serializer = question_serializer(data = ques)
				if serializer.is_valid():
					sback = serializer.save()
					sid = sback.id
					for ans in ques['options']:
						dic = {}
						dic['option_text'] = ans
						dic['question'] = sid
						new_serializer = option_serializer(data = dic)
					
						# print("Saved")
						if new_serializer.is_valid():
							instance = new_serializer.save()
						else:
							# print(serializer.errors)
							Response(new_serializer.errors)
					
				else:
					roll_back_serializer.delete()
					Response("Unknown Error")
			return Response("All THe Data has been saved")
		else:
			roll_back_serializer.delete()
			Response("Unknown Error")
