from django.db import models





class Region(models.Model):

	name = models.CharField(max_length=200)



	def __str__(self):

		return self.name


class Services(models.Model):

	name = models.CharField(max_length=200)


	def __str__(self):

		return self.name


class Applicant(models.Model):

	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	skills = models.CharField(max_length=400, null=True)
	experence = models.CharField(max_length=30, null=True)
	schedule = models.CharField(max_length=100, null=True)
	price = models.CharField(max_length=100, null=True)
	quentity = models.IntegerField(default=0)
	phone_number = models.CharField(max_length=40, null=True)
	service = models.ForeignKey(Services, on_delete=models.CASCADE)
	region = models.ForeignKey(Region, on_delete=models.CASCADE)
	is_active = models.BooleanField(default=False)
	not_received = models.BooleanField(default=False)
	chat_id = models.CharField(max_length=100, null=True)
	created_time = models.DateTimeField(auto_now_add=True)
    



	def __str__(self):

		return self.first_name+" "+self.last_name
