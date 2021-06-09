# Cloud Deployment on Google App Engine for Violence Detection API

---

Author:
* Hafizh Fauzan (M0040321)
* Charles Chang (M0040323)
* Rhennata (C1391685)
* Rosyita Ayu Sulistyo (C1391689)
* Aufa Nabil Amiri (A0040325)
* Iqbal Firmansyah (A1391686)

---

## System Overview
We will use our Machine Learning Models that detect violence and deploy it in the server so that its callable and send response when input is given.

---

## Server Deployment

### Step 1. Creating Project & Firestore & FCM
Sign in to Cloud Console and create a new project or reuse an existing one. (If you don't already have a Gmail or Google Workspace account, you must create one.)

After creating project, go to firestore and get the Auth Key, then also to FCM for Auth Key

### Step 2. Activate Cloud Shell
Then create a main.py script that contain the Model Prediction System

```
mkdir ~/bangkitCapstone
cd ~/bangkitCapstone
touch main.py
cloudshell edit main.py
```

### Step 3. Define the dependencies
To specify the dependencies of your web app, create a requirements.txt file in the root directory of your project.

```
touch requirements.txt
cloudshell edit requirements.txt
```

This is the requirements that is needed:

```
absl-py==0.12.0 
aiohttp
astor==0.8.1
astunparse==1.6.3
async-timeout==3.0.1
attrs==21.2.0 
blinker==1.4
brotlipy==0.7.0
CacheControl==0.12.6
cachetools==4.2.2
certifi==2020.12.5
cffi==1.14.5 
chardet
click==7.1.2
cryptography 
firebase-admin==5.0.0
Flask==1.1.2
gast
gevent==21.1.2
glob2==0.7
google-api-core==1.28.0
google-api-python-client==2.6.0
google-auth==1.30.0 
google-auth-httplib2==0.1.0
google-auth-oauthlib==0.4.1
google-cloud-core==1.6.0
google-cloud-firestore==2.1.1
google-cloud-storage==1.38.0
google-crc32c==1.1.2
google-pasta==0.2.0
google-resumable-media==1.3.0
googleapis-common-protos==1.53.0
greenlet==1.1.0
grpcio==1.38.0 
h5py==2.10.0
httplib2==0.19.1
idna==2.10 
importlib-metadata==4.0.1 
itsdangerous==1.1.0
Jinja2==2.11.2
Keras==2.4.3 
Keras-Applications==1.0.8
Keras-Preprocessing==1.1.2
Markdown==3.3.4
MarkupSafe==1.1.1
msgpack==1.0.2
multidict==5.1.0 
numpy
oauthlib==3.0.1
opt-einsum==3.3.0
opencv-python 
packaging==20.9
Pillow==8.2.0
proto-plus==1.18.1
protobuf==3.17.0
pyasn1==0.4.8
pyasn1-modules==0.2.7
pycparser==2.20 
pyfcm==1.5.1
PyJWT==2.1.0
pyOpenSSL==20.0.1
pyparsing==2.4.7
pyreadline==2.1 
PySocks==1.7.1 
pytz==2021.1
PyYAML==5.4.1
requests==2.25.1
requests-oauthlib==1.3.0 
rsa==4.7.2 
scipy
six==1.16.0 
tensorboard==2.4.1 
tensorboard-plugin-wit==1.8.0 
tensorflow==2.3.0
tensorflow-estimator
termcolor==1.1.0
typing-extensions==3.7.4.3
uritemplate==3.0.1
urllib3==1.26.4 
Werkzeug==1.0.1
win-inet-pton==1.1.0 
wrapt==1.12.1 
yarl==1.6.3 
zipp==3.4.1 
zope.event==4.5.0
zope.interface==5.4.0
```

### Step 4. Configure the deployment
To deploy your web app to App Engine, you need an app.yaml file. This configuration file defines your web app's settings for App Engine.

Create and edit the app.yaml file in the root directory of your project:

```
touch app.yaml
cloudshell edit app.yaml
```

Then write our configuration:

```
runtime: python38 # or another supported version

instance_class: F4_1G
```

### Step 5. Deploy the web app
Deploy your web app with the following command:

```
gcloud app deploy
```

---

## API Routes
You can start testing the system with the given URL after deployment

There are two routes:

### GET '/'
This routes send response basic HTML as a prove that our system is running. The Result should show

```
Hello World! Welcome To Violence Detection Server, Auth: Hafizh F
```


### POST '/predict'
This  routes send prediction result to firestore database and send notification to all Apps if violence detected. the input is 16 frames images that is converted to Base64 Format.

For Testing Purposes, we send 16 Image Sequences as the input that we already had.

```
import requests
import os
import base64

url = 'https://b21-cap0153adhiganawasa.et.r.appspot.com/predict'
b64_ims = []

for category in os.listdir('violence_data/'):
	with open('violence_data/' + category, 'rb') as f:
		im_b64 = base64.b64encode(f.read())
	b64_ims.append(im_b64)
	
print(len(b64_ims))

payload = {"image": b64_ims}
r = requests.post(url, data=payload)
```

For Real Product, in CCTV Stream, every 16 frame is complete, we send the data to the server.

---

## Things to Improve

* Security, as anyone currently can access the API
* Performance, there's still many unused library
