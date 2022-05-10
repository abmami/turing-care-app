from secrets import choice
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Doctor is the logged in User
# Doctor can have many Patients 
# Patient can be related to one Doctor (many to one)
# Doctor can have many Predictions
# Prediction is related to one Patient or none (many to one/none)
# Prediction is related to one Doctor (many to one)

# Doctor can manage his Patients
# Doctor can manage his Predictions
# Doctor can perform Predictions (either related to one Patient or none)


class Patient(models.Model):
   # 'first_name', 'last_name', 'birthday', 'email', 'gender', 'address', 'city', 'zip_code', 'phone'
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    birthday = models.DateTimeField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True,)
    status = models.CharField(max_length=50, default="active")
    genders = [('Male','Male'), ('Female','Female'),('Other','Other')]
    gender = models.CharField(choices=genders, max_length=50)
    address = models.CharField(null=True, blank=True,max_length=200, default='None')  
    city = models.CharField(null=True, blank=True,max_length=200)  
    states = [('Tunis','Tunis'), ('Nabeul','Nabeul'),('Sousse','Sousse')]
    state = models.CharField(null=True, blank=True,choices=states, max_length=100)
    zip_code = models.CharField(null=True, blank=True,max_length=50, default='None')  
    phone = models.CharField(null=True, blank=True,max_length=50)  
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)


class Prediction(models.Model):
    covid19 =  models.CharField(max_length=50, default='None')
    dominant_class =  models.CharField(default='None',max_length=50)
    normal =  models.CharField(default='None',max_length=50)
    pneumonia = models.CharField(default='None',max_length=50)
    tuberculosis = models.CharField(default='None',max_length=50)
    uploaded_image = models.ImageField(upload_to='raw', blank=True)
    heatmap = models.ImageField(upload_to='heatmap', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="active") 
    comment = models.CharField(default='None',max_length=200) #patient related comment
    feedbacks = [('Correct','Correct'),('covid19','covid19'),('normal','normal'),('pneumonia','pneumonia'),('tuberculosis','tuberculosis')]
    model_feedback = models.CharField(default='Correct',choices=feedbacks, max_length=100) #model related feedback
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)


