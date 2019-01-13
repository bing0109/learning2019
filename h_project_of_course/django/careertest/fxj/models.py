from django.db import models

# Create your models here.
class Qustion(models.Model):
    name=models.CharField(max_length=200)
    qustion_type=models.CharField(max_length=100)
    isdelete=models.BooleanField(default=False)
class Answer(models.Model):
    content=models.CharField(max_length=2048)
    question_id=models.ForeignKey(to='Qustion',on_delete=models.CASCADE)
    factor1_value=models.DecimalField(max_digits=5,decimal_places=2)
    factor2_value=models.DecimalField(max_digits=5,decimal_places=2)
    factor3_value=models.DecimalField(max_digits=5,decimal_places=2)
    factor4_value=models.DecimalField(max_digits=5,decimal_places=2)
    factor5_value=models.DecimalField(max_digits=5,decimal_places=2)
    factor6_value=models.DecimalField(max_digits=5,decimal_places=2)
    factor7_value=models.DecimalField(max_digits=5,decimal_places=2)
    factor8_value=models.DecimalField(max_digits=5,decimal_places=2)
    factor9_value=models.DecimalField(max_digits=5,decimal_places=2)
    factor10_value=models.DecimalField(max_digits=5,decimal_places=2)
    isdelete=models.BooleanField(default=False)