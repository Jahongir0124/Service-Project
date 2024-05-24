from django.urls import path
from . views import *

urlpatterns = [
	
	path('', GetRegion.as_view()),
	path('getService', GetServiceView.as_view()),
	path('getApplicant', GetApplicantView.as_view()),
	path('getApplicantdetail', GetApplicantDetailView.as_view()),
	path('createApplicant', CreateApplicantView.as_view()),
	path('control', controlView, name='control'),
	path('applicantDetailView/<int:id>', applicantDetailView, name="detailView"),
	path('conform/<int:id>', confirmationView, name="conform"),
	path('cancel/<int:id>', cancellationView, name='cancel'),
	path("loginView", loginView, name="login")

]