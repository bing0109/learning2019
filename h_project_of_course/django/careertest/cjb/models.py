from django.db import models
from zjj.models import Tester, Jobneed
# Create your models here.


class Testchart(models.Model):
    teser_id = models.ForeignKey(to=Tester, on_delete=models.CASCADE)
    jobneed_id = models.ForeignKey(to=Jobneed, on_delete=models.CASCADE)
    link = models.CharField(max_length=512)
    status = models.IntegerField()
    isdelete = models.BooleanField(default=False)


class Report(models.Model):
    testchart_id = models.ForeignKey(to='Testchart', on_delete=models.CASCADE)
    factor1_total_value = models.DecimalField(max_digits=5, decimal_places=2)
    factor2_total_value = models.DecimalField(max_digits=5, decimal_places=2)
    factor3_total_value = models.DecimalField(max_digits=5, decimal_places=2)
    factor4_total_value = models.DecimalField(max_digits=5, decimal_places=2)
    factor5_total_value = models.DecimalField(max_digits=5, decimal_places=2)
    factor6_total_value = models.DecimalField(max_digits=5, decimal_places=2)
    factor7_total_value = models.DecimalField(max_digits=5, decimal_places=2)
    factor8_total_value = models.DecimalField(max_digits=5, decimal_places=2)
    factor9_total_value = models.DecimalField(max_digits=5, decimal_places=2)
    factor10_total_value = models.DecimalField(max_digits=5, decimal_places=2)
    quetoans = models.CharField(max_length=2048)
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()



