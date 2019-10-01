# PROJECT NOAH

![](https://dl0.creation.com/articles/p074/c07490/NoahsArkFlood.jpg)

## INTRODUCTION
__Project Noah__ is a independent project that attempts to address various environment issues using Data and Machine Learning.

## VIETNAM AIR QUALITY INDEX

__Vietnam Air Quality Index (Vietnam AQI)__ is a first module of the __Project Noah__. Its main purpose is to collect and visualize the data of Air Quality in major cities in Vietnam. The data is collected hourly from the API of [The World Air Quality Index project](http://aqicn.org/api/).

The collection is done by a Python Script running on __Google Cloud's Compute Engine__ and data is stored on __Google Cloud's BigQuery__, which is then visualized on __[Google Data Studio](https://datastudio.google.com/u/0/reporting/1lqZ8zNIVrH4C_apLcPOOniV_pGKr83NN/page/vFg1)__.

### Guide

__Setup API__
- [Register](http://aqicn.org/data-platform/token/) for API Token

__Setup Google Cloud APIs__
- Create Project
- Enable APIs for __Compute Engine, BigQuery, Storage__
- Download [Authentication Key](https://console.cloud.google.com/apis/credentials/serviceaccountkey?_ga=2.227289245.-1007630523.1565869255&_gac=1.52611100.1569826292.EAIaIQobChMIvay9wPr35AIVF7eWCh1T8Q8IEAAYASAAEgIt7fD_BwE)

_Google Cloud Storage_
- Create Google Cloud Storage bucket
- Upload `noah.py`, `requirement.txt` and Authentication Key to bucket

_Compute Engine_
- Create VM instance. Having ~ 1 Gb of Memory should be enough.
- SSH VM Instance. 
- Install pip
```
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
```

Copy `noah.py`, `requirement.txt` and Authentication Key to VM.
 
```
mkdir noah
gsutil cp gs://<bucket_name>/<file_name> noah
```

_BigQuery_
- Create BigQuery Database
- Create table with Schema: 

| Field name   |      Type      |  Mode |
|----------|:-------------:|------:|
| ID |  INTEGER | REQUIRED |
| Time |    TIME   |   REQUIRED |
| Date | DATE |    REQUIRED |
| City | STRING |    REQUIRED |
| AQI | FLOAT |    REQUIRED |
| DominentPol | STRING |    REQUIRED |
| CO | FLOAT |    REQUIRED |
| NO2 | FLOAT |    REQUIRED |
| O3 | FLOAT |    REQUIRED |
| PM25 | FLOAT |    REQUIRED |
| Dew | FLOAT |    REQUIRED |

__Virtual environment__
- Create virtual environment
```
cd noah
virtualenv noah-env
```

- Activate virtual environment
```
source noah-env/bin/activate
```

- Install libraries in virtual environment
```
sudo pip install -r requirement.txt
```
- Set environment variable for Google Application Credentials 
```
export GOOGLE_APPLICATION_CREDENTIALS='path/to/json_file'
```

__Running the Script__
- Edit User Settings in `noah.py`
```
vim noah.py
```
 - Make `noah.py` executable
 ```
 chmod +x ./noah.py
 ```
 - Run `noah.py` in background
 ```
 nohup stdbuf -oL ./noah.py > log.out &
 ```
 With `nohup` and `&` in the end we can keep the script running in the background, even after logging out. 
 To  make sure that the script is running:
 ```
 ps ax | grep noah.py
 ```
 To terminate the script:
 ```
 kill PID
 ```
 To see the output of the script:
 ```
 cat ./log.out
 ```