from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from . models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from . serializer import *
import requests
from django.db.models import Q
from django.db.models.signals import pre_save
from django.dispatch import receiver
from . send_request import *
import time
from django.apps import AppConfig
from django.core.signals import setting_changed
from django.contrib.auth import authenticate, login, logout
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
bot_token = ''
	


class GetRegion(generics.ListAPIView):

	queryset = Region.objects.all()
	serializer_class = RegionSerializer


class GetServiceView(generics.ListAPIView):


	queryset = Services.objects.all()
	serializer_class = ServiceSerializer

class GetApplicantView(generics.ListAPIView):

	queryset = Applicant.objects.all()
	serializer_class = ApplicantSerializer

	def list(self, request):
		service_id = request.GET.get('sname')
		region_id = request.GET.get('region')
		applicant = Applicant.objects.filter(service_id=service_id).filter(region_id=region_id).filter(is_active=True)
		serializer = self.serializer_class(applicant, many=True)
		return Response(serializer.data, status=200)


class GetApplicantDetailView(generics.ListAPIView):

	queryset = Applicant.objects.all()
	serializer_class = ApplicantDetailSerialzier


	def list(self, request):

		appId = request.GET.get('id')
		applicant = get_object_or_404(Applicant, pk=appId)
		serializer = self.serializer_class(applicant)
		return Response(serializer.data, status=200)


class CreateApplicantView(generics.ListCreateAPIView):

	queryset = Applicant.objects.all()
	serializer_class = ApplicantDetailSerialzier

	def post(self, request):


		fname = request.data['first_name']
		lname = request.data['last_name']
		experence = request.data['year_experence']
		phone_number = request.data['phone_number']
		serviceID = request.data['service']
		regionID = request.data['region']
		skills = request.data['skills']
		price = request.data['price']
		service = Services.objects.get(pk=serviceID)
		region = Region.objects.get(pk=regionID)
		chat_id = request.data['chat_id']
		schedule = request.data['schedule']
		applicant = Applicant.objects.create(
			first_name=fname,
			last_name=lname,
			experence=experence,
			skills=skills,
			schedule=schedule,
			price=price,
			phone_number=phone_number,
			service=service,
			region=region,
			chat_id=chat_id
			) 
		return Response({'Created': True}, status=201)



def loginView(request):
	if request.POST:
		uname = request.POST.get("username")
		password = request.POST.get("password")
		user = authenticate(request, username=uname, password=password)
		if user:
			login(request, user)
			request.session['time_login'] = datetime.now().strftime('%Y-%m-%d %H:%M')
			return redirect('control')

		else:
			return redirect('login')
	return render(request, 'login.html')


def controlView(request):
	if request.user.is_authenticated:
		applicant = Applicant.objects.all().order_by('-created_time')
		return render(request, 'index.html', {'applicant': applicant})
	else:
		return redirect('login')

def applicantDetailView(request, id):
	if request.user.is_authenticated:
		applicant = Applicant.objects.get(pk=id)

		return render(request, 'detail.html', {'applicant': applicant})
	else:
		return redirect('login')

def confirmationView(request, id):
	if request.user.is_authenticated:
		applicant = Applicant.objects.get(pk=id)
		applicant.is_active = True

		text = """
Подтверждение:

🎉 Приветствуем вас в нашем 
сообществе! 🤝 Ваша заявка 
рассмотрена, и мы с удовольствием 
сообщаем, что вы подходите для 
сотрудничества. 🚀 В ближайшее время наш представитель свяжется с вами 
для дальнейших шагов. 
Спасибо за выбор нас!"""
		url = f"https://api.telegram.org/{bot_token}/sendMessage?chat_id={applicant.chat_id}&text={text}"
		r = requests.post(url, json={})
		applicant.save()
		return redirect('control')
	else:
		return redirect('login')

def cancellationView(request, id):
	if request.user.is_authenticated:
		applicant = Applicant.objects.get(pk=id)
		text = """
Отказ:

😔 Благодарим вас за интерес к нашему 
сообществу. К сожалению, после 
внимательного рассмотрения мы не 
можем предложить вам сотрудничество 
в настоящее время. Надеемся на ваше 
понимание и желаем успехов в поиске 
подходящей возможности. Спасибо за 
проявленный интерес."""

		url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={applicant.chat_id}&text={text}"
		r = requests.post(url, json={})
		applicant.delete()
		return redirect('control')

	else:
		return redirect('login')








