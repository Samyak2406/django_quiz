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

class option_serializer(serializers.ModelSerializer):
	class Meta:
		model = Option
		fields = '__all__'

class submission_serializer(serializers.ModelSerializer):
	class Meta:
		model = Submission
		fields = '__all__'
