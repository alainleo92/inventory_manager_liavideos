from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login
from .forms import UserRegisterForm

# Create your views here.
class SignUpView(View):
	def get(self, request):
		form = UserRegisterForm()
		return render(request, 'users/signup.html', {'form': form})
	def post(self, request):
		form = UserRegisterForm(request.POST)

		if form.is_valid():
			form.save()
			user = authenticate(
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password1']
			)

			login(request, user)
			return redirect('index')

		return render(request, 'users/signup.html', {'form': form, 'title': "Signup"})
