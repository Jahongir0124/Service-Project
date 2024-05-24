from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import auth
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate, login, logout


class AutoLogout(object):


	def __init__(self, get_response):

		self.get_response = get_response

	def __call__(self, request):
		response = self.get_response(request)
		try:
			last_login = datetime.strptime(request.session['time_login'],"%Y-%m-%d %H:%M")
			compire_time = (datetime.now()-last_login).total_seconds()
			if compire_time>4:
				logout(request)
				del request.session['time_login']

			else:
				request.session['time_login'] = datetime.now().strftime('%Y-%m-%d %H:%M')
			return response
			
		except Exception as e:
			print(e)
		return response