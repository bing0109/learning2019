from django.db import models
# Create your models here.
class UserAdmin(models.Model):
	user=models.CharField(max_length=20)
	password=models.CharField(max_length=20)
	email=models.EmailField()
	isdelete=models.BooleanField(default=False)


class UserHR(models.Model):
	user=models.CharField(max_length=20)
	password=models.CharField(max_length=20)
	hrname = models.CharField(max_length=100,null=True,blank=True)
	email=models.EmailField()
	company_id=models.ForeignKey(to='Company',on_delete=models.CASCADE)
	isdelete=models.BooleanField(default=False)

class UserExpert(models.Model):
	user=models.CharField(max_length=20)
	password=models.CharField(max_length=20)
	email=models.EmailField()
	isdelete=models.BooleanField(default=False)


class Company(models.Model):
	logo=models.ImageField()
	name=models.CharField(max_length=100)
	info=models.TextField()
	isdelete=models.BooleanField(default=False)

class Factor(models.Model):
	name=models.CharField(max_length=100)
	isdelete=models.BooleanField(default=False)


class Moding(models.Model):
	name=models.CharField(max_length=100)
	isdelete=models.BooleanField(default=False)

class ModelDesign(models.Model):
	moding_id = models.ForeignKey(to='Moding',on_delete=models.CASCADE)
	factor_id = models.ForeignKey(to='Factor', on_delete=models.CASCADE)
	factor_ex_value = models.DecimalField(max_digits=5, decimal_places=2)
	isdelete=models.BooleanField(default=False)
