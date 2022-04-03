from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.
from django.forms import HiddenInput

from home.models import Profile


class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user


class EditProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = [
			'user',
			'description',
			'birth_date',
			'profile_picture',
		]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['user'].disabled = True
		self.fields['user'].widget = HiddenInput()


class EditUserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = [
			'username',
			'first_name',
			'last_name',
		]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

