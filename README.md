# ttrs-backend

## Initial Setting
### virtual environment
```console
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ sudo apt-get install python3 python3-dev python3-pip
$ pip3 install django djangorestframework selenium
```
```console
$ git clone https://github.com/SWPP/ttrs-backend.git
```

## Notice
#### Crawling in server machine
Installing chromium-browser and downgrading selenium seems to work.
```console
$ sudo apt-get install chromium-browser
$ pip3 uninstall selenium
$ pip3 install selenium==3.10
```

## APIs
For the specification, please see **Issue**
#### [Student](#11)
- **student/**
  - *get*: get student list
  - *post*: create new student
- **student/\<int:pk\>/**
  - *get*: get the student
  - *put*: replace information of the student
  - *patch*: update information of the student
  - *delete*: delete the student 

#### Crawler
**Note:** this api is only for the *admin users*
- **crawlers/**
  - *get*: get crawler list
  - *post*: create new crawler and start
- **crawlers/\<int:pk\>/**
  - *get*: get the crawler
  - *put/patch*: cancel the crawler
  - *delete*: delete the crawler

## ttrs-frontend
https://github.com/SWPP/ttrs-frontend
