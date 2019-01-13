from django.db import models
from qsj.models import Company,Moding,UserAdmin,UserHR,UserExpert,Factor,ModelDesign


# Create your models here.
class Job(models.Model):
    jobname=models.CharField(max_length=100)    # 添加的时候，逻辑里面要判断不能重复
    moding_id=models.ForeignKey(to=Moding,on_delete=models.CASCADE)
    isdelete=models.BooleanField(default=False)


class Jobneed(models.Model):
    job_id = models.ForeignKey(to='Job',on_delete=models.CASCADE,null=True,blank=True)
    jobneed_name = models.CharField(max_length=100,default='')     # 职位需求名称，默认和关联的职位名称一致
    jobdescription=models.CharField(max_length=1024)
    jobrequirements=models.CharField(max_length=1024)
    moding_id=models.ForeignKey(to=Moding,on_delete=models.CASCADE, null=True, blank=True)
    isdelete=models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now=True)   # 创建时间
    create_hr_id = models.ForeignKey(to=UserHR, on_delete=models.CASCADE, null=True, blank=True)   # 创建人，可以关联到hr
    jobneed_status = models.IntegerField(default=1)  # 职位需求状态，1：招聘中，0：招聘结束，2：模型定制中


class Tester(models.Model):
    name=models.CharField(max_length=20)
    jobneed_id=models.ForeignKey(to='Jobneed', on_delete=models.CASCADE,null=True,blank=True)
    sex=models.BooleanField(default=True)
    comment=models.CharField(max_length=1024)
    create_hr_id = models.ForeignKey(to=UserHR, on_delete=models.CASCADE, null=True, blank=True)   # 创建人，可以关联到hr
    status=models.IntegerField(default=1)  # 求职者状态，0：未邀请测试，1：已邀请测试，2：测试完成，3：通过测试，4：淘汰
    isdelete=models.BooleanField(default=False)
