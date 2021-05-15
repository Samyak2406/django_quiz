from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Quiz_Details)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Submission)