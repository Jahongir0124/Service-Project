from . models import *
import requests
import time

def sendRequestFunc(appId):


	if appId:
		applicant = Applicant.objects.get(pk=appId)
		print(applicant.is_active)


