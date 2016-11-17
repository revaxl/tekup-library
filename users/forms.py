from django import forms
from django.contrib.auth import get_user_model

from authtools.forms import UserChangeForm

User = get_user_model()

class updateProfile(UserChangeForm):
	class Meta:
		model = User
		fields = ['email', 'name','password', 'password']