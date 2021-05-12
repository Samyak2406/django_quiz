from rest_framework import serializers
from .models import *

class quiz_serializer(serializers.ModelSerializer):
	class Meta:
		model = Quiz_Details
		fields = '__all__' 


class question_serializer(serializers.ModelSerializer):
	class Meta:
		model = Question
		fields = '__all__'

class answer_serializer(serializers.ModelSerializer):
	class Meta:
		model = Answer
		fields = '__all__'

class submission_serializer(serializers.ModelSerializer):
	class Meta:
		model = Submission
		fields = '__all__'

# Checkiing Serializers

# class question_serializer_check(serializers.ModelSerializer):
# 	class Meta:
# 		model = Question
# 		fields = ['question_text']

# class answer_serializer_check(serializers.ModelSerializer):
# 	class Meta:
# 		model = Answer
# 		fields = ['answer_text']