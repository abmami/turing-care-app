# TuringCare - Lung Disease Management Application
*TuringCare is an academic project developed in the framework of AI studies at [ESPRIT] by [TuringTeam]*
#### _Initial Release v1.0_
TuringCare enables fast and effective disease response by providing an easy management and access to patient information at one place. The TuringCare web app also allows healthcare professionals to early detect lung diseases (Covid-19, Tuberculosis, Viral Pneumonia) in Chest X-Ray images and link results to patients' records. The TuringCare app uses Artificial Intelligence to classify diseases and interpret abnormalities in the lungs from Chest X-Ray images.

## Features

##### Account & Authentification
- Register an account.
- Log in into an account.
- Update account informations.


##### Patients Management
- Create a new patient.
- View a patient record (general information, related model prediction results).
- View all patients.
- Update a patient.
- Delete a patient.


##### Predictions Management
- Import and classify a Chest X-Ray image using CNN deep learning model.
- View prediction results.
- View all predictions.
- Update a prediction (link Chest X-Ray to a patient, enter feedback).
- Delete a prediction.


## Tech
TuringCare uses open source projects and frameworks to work properly:
- [Django] - a python-based free and open-source web framework.
- [Bootstrap 5] - a free and open-source CSS framework directed at responsive, mobile-first front-end web development.
- [TensorFlow] - a free and open-source software library for machine learning and artificial intelligence.
- [Volt Django Dashboard] - a free and open source Django Dashboard Template.

And of course TuringCare itself is open source with a [public repository](https://github.com/abdessalemmami/turing-care-app)
 on GitHub.

## Installation
**Step 1:** Install tools
- [Git](https://git-scm.com/download/win)
- [NodeJS](https://nodejs.org/en/) 12.x or higher
- [Gulp](https://gulpjs.com/) - globally 
    - `npm install -g gulp-cli`

**Step 2:** Clone Repo
```bash
git clone https://github.com/abdessalemmami/turing-care-app.git
```
**Step 3:** Install Node Modules 
```bash
cd apps/static/assets
npm install
```
**Step 4:** Edit & Recompile SCSS files 
```bash
gulp scss
```
**Step 5:** Configure Virtual Environment
```bash
cd turing-care-app
pip install virtualenv
virtualenv env
.\env\Scripts\activate
pip3 install -r requirements.txt
```

**Step 6:** Create Database Tables
```bash
python manage.py makemigrations
python manage.py migrate
```
**Step 7:** Run Development Server
```bash
python manage.py runserver
```
Access the web app in your preferred browser (http://127.0.0.1:8000/) and that's it!

## Team
- [Arij Boubaker](https://www.linkedin.com/in/arij-boubaker/) - AI Enginnering Student, ESPRIT
- [Abdessalem Mami](https://www.linkedin.com/in/abdessalem-mami/) - AI Enginnering Student, ESPRIT
- [Adem Boukhris](https://www.linkedin.com/) - AI Enginnering Student, ESPRIT
- [Mohamed Fathallah](https://www.linkedin.com/in/medfathallah/) - AI Enginnering Student, ESPRIT
- [Firas Soltani](https://www.linkedin.com/) - AI Enginnering Student, ESPRIT

## License
MIT



[//]: # (refs)

   [TuringCare]: <https://github.com/abdessalemmami/turing-care-app>
   [git-repo-url]: <https://github.com/abdessalemmami/turing-care-app>
   [Django]: <https://www.djangoproject.com/>
   [Bootstrap 5]: <https://getbootstrap.com/>
   [Tensorflow]: <https://www.tensorflow.org/>
   [Volt Django Dashboard]: <https://themesberg.com/product/django/volt-admin-dashboard-template>
   [ESPRIT]: <https://esprit.tn/>
   [TuringTeam]: <>