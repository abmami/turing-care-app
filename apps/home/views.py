from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import * 
from .forms import * 
from django.shortcuts import get_object_or_404, redirect, render
from datetime import date

def log(action, user):
    today = date.today().strftime("%b-%d-%Y")
    d = {'date':today, 'user':user, 'action':action}
    print(d)

@login_required(login_url="/login/")
def index(request):
    kpis = {"total_predictions":getKPI("total_predictions", user=request.user),
    "total_patients":getKPI("total_patients", user=request.user),
    }
    context = {'segment': 'index', 'kpis':kpis}


    html_template = loader.get_template('home/dashboard.html')
    return HttpResponse(html_template.render(context, request))


#@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))



##### PATIENTS MANAGEMENT VIEWS #####

# VIEW ALL PATIENTS #
@login_required(login_url="/login/")
def view_patients(request):
    loggedUser = request.user
    patients = Patient.objects.filter(doctor=loggedUser, status="active")
    kpis = {"total_patients":getKPI("total_patients", user=request.user),
                "recent_added_patient":getKPI("recent_added_patient", user=request.user),
                "recent_xr_patient":getKPI("recent_xr_patient", user=request.user),
    }
    context = {'segment': 'view_patients', 'patients':patients, 'kpis':kpis}

    html_template = loader.get_template('home/patients/view_patients.html')
    return HttpResponse(html_template.render(context, request))

# ADD NEW PATIENT #
@login_required(login_url="/login/")
def add_patient(request):
    #context = {'segment': 'add_patient'}
    if request.method == 'POST':
        form = AddPatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.doctor = request.user
            patient.save()
            log("added a patient", request.user.username)
            return redirect('view_patients')
        else:
             return render(request,'home/patients/add_patient.html',{'form': form,'segment': 'add_patient'})

    else:
        form = AddPatientForm()
    return render(request,'home/patients/add_patient.html',{'form': form,'segment': 'add_patient'})


# VIEW PATIENT RECORD #
@login_required(login_url="/login/")
def view_patient(request, id):
    # retrieve patient details
    patient = Patient.objects.get(pk=int(id))
    # retrieve related predictions to this patient
    predictions = Prediction.objects.filter(patient=patient, status="active")
    
    context = {'segment': 'view_patient', 'patient':patient, 'predictions':predictions}

    html_template = loader.get_template('home/patients/view_patient.html')
    return HttpResponse(html_template.render(context, request))


# DELETE PATIENT # 
@login_required(login_url="/login/")
def delete_patient(request,id):
    patient = Patient.objects.get(pk=int(id))
    if patient:
        log("deleted a patient",request.user.username)
        patient.status = "deleted"
        patient.save()
    return redirect('view_patients')


# UPDATE PATIENT # 
@login_required(login_url="/login/")
def update_patient(request,id):
    if request.method == 'POST':
        form = UpdatePatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.doctor = request.user
            patient.save()
            log("updated a patient", request.user.username)
            return redirect('update_patient')
        else:
             return render(request,'home/patients/update_patient.html',{'form': form,'segment': 'update_patient'})

    else:
        patient = Patient.objects.get(pk=int(id))
        #'first_name', 'last_name', 'birthday', 'email', 'gender', 'address', 'state', 'city', 'zip_code', 'phone'
        form = UpdatePatientForm()
    return render(request,'home/patients/update_patient.html',{'form': form,'segment': 'update_patient', 'patient':patient})


def doesAccountHave(check,user):
    if check == "predictions":
        predictions = Prediction.objects.filter(status="active", doctor=user)
        return predictions.count() != 0
    else:
        patients = Patient.objects.filter(status="active", doctor=user)
        return patients.count() != 0

    

from django.db.models import Count
#### KPIs API #####
def getKPI(name, user=None):
    predictions = Prediction.objects.filter(status="active", doctor=user)
    patients = Patient.objects.filter(status="active", doctor=user)
    
    if name == "total_predictions":
        return predictions.count()
    elif name == "most_frequent_class":
        if predictions.count() == 0:
            return "Unavailable"
        query = predictions.values('dominant_class').order_by().annotate(count=Count('dominant_class'))
        maxval = max(query, key=lambda x:x['count'])
        return maxval['dominant_class']
    elif name == "least_frequent_class":
        if predictions.count() == 0:
            return "Unavailable"        
        query = predictions.values('dominant_class').order_by().annotate(count=Count('dominant_class'))
        minval= min(query, key=lambda x:x['count'])
        return minval['dominant_class']
    elif name == "total_patients":
        return patients.count()
    elif name == "recent_added_patient":
        rap = patients.order_by('-created_at').filter(doctor=user).first()
        if rap:
            return rap.id
        else:
            return "Unavailable"
    elif name == "recent_xr_patient":
        rxrp = predictions.order_by('-created_at').filter(doctor=user).exclude(patient__isnull=True).first()
        if rxrp:
            return rxrp.patient.id
        else:
            return "Unavailable"
    else:
        return "wrong kpi name"


##### PREDICTIONS MANAGEMENT VIEWS #####

# VIEW ALL PREDICTIONS #
@login_required(login_url="/login/")
def view_predictions(request):
    predictions = Prediction.objects.order_by('-created_at').filter(doctor=request.user)
    kpis = {"total_predictions":getKPI("total_predictions", user=request.user),
                "most_frequent_class":getKPI("most_frequent_class", user=request.user),
                "least_frequent_class":getKPI("least_frequent_class", user=request.user),
    }
  
    context = {'segment': 'view_predictions', 'predictions':predictions,'kpis':kpis}

    html_template = loader.get_template('home/predictions/view_predictions.html')
    return HttpResponse(html_template.render(context, request))


# ADD NEW PREDICTION #
@login_required(login_url="/login/")
def new_prediction(request):
    context = {'segment': 'new_prediction'}

    html_template = loader.get_template('home/predictions/new_prediction.html')
    return HttpResponse(html_template.render(context, request))


# LOADING CNN MODEL #  


import PIL
from PIL import Image
import numpy as np
import tensorflow as tf
import requests
from keras.models import load_model
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from .deep import *
# if you change the model, make sure you change last conv layer name for the GRAMCAM to work  if the model architecture is different
#modelcnn = load_model("apps\deepmodels\model_fpl.h5")
modelcnn = load_model("apps\deepmodels\model_fpl2.h5")
from django.core.files import File

import time
# UPLOAD X-RAY #
@login_required(login_url="/login/")
def upload_predict(request):
    if  request.method == "POST" and 'uploadImageBtn' in request.POST:
        # Getting uploaded image
        f=request.FILES['XRFILE'] 
        prediction = Prediction(doctor=request.user, uploaded_image=f)
        prediction.save()
        # Predicting class
        testimage = prediction.uploaded_image.path
 
        img = load_img(testimage, target_size=(150, 150))
        numpy_image = img_to_array(img)
        results = predict_image(modelcnn,numpy_image)
        # Saving model results 
        prediction.covid19 = results['covid19']
        prediction.tuberculosis = results['tuberculosis']
        prediction.normal = results['normal']
        prediction.pneumonia = results['pneumonia']
        # Saving dominant class
        mk = list(results.keys())
        mv = list(results.values())
        prediction.dominant_class = mk[mv.index(max(mv))]
        prediction.save()
        # GRAMCAM 
        # can be optimized : return prediction results + heatmap in a single flow
        fs = FileSystemStorage()
        overlay = toGRADCAM(testimage, modelcnn)
        overlay_path = fs.location+"/temp.png"
        overlay.save(overlay_path)
        x = open(overlay_path, 'rb')
        content = File(x)
        print(content.name)
        prediction.heatmap.save(f.name, content, save=True)
        return redirect('update_prediction', prediction.id)

# VIEW PREDICTION #
@login_required(login_url="/login/")
def view_prediction(request, id):
    prediction = Prediction.objects.get(pk=int(id))  
    results = {'covid19':prediction.covid19,'tuberculosis':prediction.tuberculosis,'normal':prediction.normal,'pneumonia':prediction.pneumonia}
    context = {'segment': 'view_prediction', 'prediction':prediction, 'results':results}
    html_template = loader.get_template('home/predictions/view_prediction.html')
    return HttpResponse(html_template.render(context, request))


# UPDATE PREDICTION #
@login_required(login_url="/login/")
def update_prediction(request, id):
    if request.method == "POST":
        form = UpdatePrediction(request.POST) #somehow its bugging so let's manually retrieve feedback
        if form.is_valid():
            current_pred = Prediction.objects.get(pk=int(id))
            p_id = request.POST['patientSelect']
            feedback = request.POST['model_feedback']
            #prediction = form.save(commit=False)
            current_pred.model_feedback = feedback
            if p_id == "Unassigned":
                current_pred.patient = None
            else:
                 current_pred.patient = Patient.objects.get(pk=int(p_id))
            current_pred.save()
            return redirect("update_prediction",id=id)

    else:
        prediction = Prediction.objects.get(pk=int(id))  
        results = {'covid19':prediction.covid19,'tuberculosis':prediction.tuberculosis,'normal':prediction.normal,'pneumonia':prediction.pneumonia}
        uform = UpdatePrediction()
        patients = Patient.objects.order_by('first_name').filter(doctor=request.user, status="active")
        context = {'segment': 'update_prediction','prediction': prediction, 'results':results, 'uform':uform, 'patients':patients}
        html_template = loader.get_template('home/predictions/update_prediction.html')
        return HttpResponse(html_template.render(context, request))

# DELETE PREDICTION #
@login_required(login_url="/login/")
def delete_prediction(request,id):
    prediction = Prediction.objects.get(pk=int(id))
    if prediction:
        log("deleted a prediction",request.user.username)
        prediction.status = "deleted"
        prediction.save()
    return redirect('view_predictions')


## OTHER STUFF ##

@login_required(login_url="/login/")
def settings(request):
    context = {'segment': 'settings'}

    html_template = loader.get_template('home/settings.html')
    return HttpResponse(html_template.render(context, request))






