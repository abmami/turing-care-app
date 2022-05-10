from django.urls import path, re_path
from apps.home import views


urlpatterns = [

    # DASHBOARD #
    path('', views.index, name='home'), #dashboard landing page

    # PATIENTS MANAGEMENT URLS #
    path('patients', views.view_patients, name = 'view_patients'), 
    path('patients/add-patient', views.add_patient, name = 'add_patient'), 
    path('patients/update-patient/<int:id>', views.update_patient, name = 'update_patient'), 
    path('patients/view-patient/<int:id>', views.view_patient, name = 'view_patient'), 
    path('patients/delete-patient/<int:id>', views.delete_patient, name = 'delete_patient'),

    # PREDICTIONS MANAGEMENT URLS #
    path('predictions', views.view_predictions, name = 'view_predictions'),
    path('predictions/delete-prediction/<int:id>', views.delete_prediction, name = 'delete_prediction'),
    path('predictions/view-prediction/<int:id>', views.view_prediction, name = 'view_prediction'),
    path('predictions/update-prediction/<int:id>', views.update_prediction, name = 'update_prediction'),
    path('predictions/new-prediction', views.new_prediction, name = 'new_prediction'), 
    path('predictions/predict', views.upload_predict, name = 'upload_predict'),

    # OTHER PAGES #
    path('settings', views.settings, name = 'settings') #settings page

    


    # Matches any html file
    #re_path(r'^.*\.*', views.pages, name='pages'),

] 
