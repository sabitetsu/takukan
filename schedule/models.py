
from django.db import models

# class ScheduleModel(models.Model):
#     userID = models.CharField(max_length=50)
#     scheduleDate = models.ArrayField(base_field=models.DateField())

class UserModel(models.Model):
    userID = models.CharField(primary_key=True, max_length=50)
    userName = models.CharField(max_length=100)
    profile = models.CharField(max_length=300)
    def __str__(self):
        return self.userID

class TakuModel(models.Model):
    takuID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    charaURL = models.CharField(max_length=300)
    def __str__(self):
        return self.title

class TakuDate(models.Model):
    takuID = models.ForeignKey(TakuModel,on_delete=models.CASCADE)
    date = models.DateTimeField()

class TakuMember(models.Model):
    takuID = models.ForeignKey(TakuModel,on_delete=models.CASCADE)
    member = models.CharField(max_length=100)

STATUS = (('CREATE','クリエイト'),('EDIT','エディット'),('SUBMIT','サブミット'))
class TakuSuke(models.Model):
    takusukeID = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100,blank=True)
    member = models.CharField(max_length=500,blank=True)
    submitDate = models.CharField(max_length=500,blank=True)
    status = models.CharField(max_length=50,choices=STATUS,blank=True)

class PersonalSchedule(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=200,blank=True)
    member = models.CharField(max_length=1000,blank=True)
    date = models.CharField(max_length=1000,blank=True)


# class UserModel:


# ScheduleModel().scheduleDate

# toppings = models.ManyToManyField(topping)

# schedate={
#     takusuke
#     takusuke
# }