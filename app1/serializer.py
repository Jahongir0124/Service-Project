from rest_framework.serializers import ModelSerializer
from . models import *


class RegionSerializer(ModelSerializer):


	class Meta:

		model = Region
		fields = '__all__'


class ServiceSerializer(ModelSerializer):

	class Meta:

		model = Services
		fields = '__all__'


class ApplicantSerializer(ModelSerializer):

	class Meta:

		model = Applicant
		fields = ["id", "first_name", "last_name"]


class ApplicantDetailSerialzier(ModelSerializer):


	class Meta:

		model = Applicant
		fields = '__all__'