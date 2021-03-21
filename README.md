# Text Messages Automation Tool 📱


[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CircleCI Status](https://circleci.com/gh/Pierre-Alexandre35/messaging-service-mousset.svg?style=shield&circle-token=:circle-token)](https://circleci.com/gh/Pierre-Alexandre35/messaging-service-mousset)

[![codecov](https://codecov.io/gh/Pierre-Alexandre35/messaging-service-mousset/branch/main/graph/badge.svg?token=2O5LYO9M7G)](https://codecov.io/gh/Pierre-Alexandre35/messaging-service-mousset)


## Description
Platform to send text messages to individuals or groups of customers in 1 click.


## Context
My parents have a small retail business and they are storing informations about their customers on a small Microsoft Excel file. Since 2018, they are doing 2 to 3 SMS text message marketing campaigns every year. They have 2 issues:
1) They could not send +1,000 text messages with a single phone. They had to use multiple phones which was not really reliable. 
2) It took them multiple hours for each campaigns to text every customers. 

We had to build a easy-to-use tool for them to let them text their customers in one click. 

## Instalation 
```git clone```
<br>

```virtualenv dev-env```
<br>

```pip3 -r install requirements.txt```
<br>

```export FLASK_APP=web_messaging/app.py```
<br>

```flask run```


## Architecture
- Front-End: Jinja2 / Bootstrap / HTML
- Back-End: Flask / Python 
- Database: MongoDB 
- Hosting: Cloud Run (Google)


## Roadmap
- Add Twilio balance $ on the navar  
- Single page to create, delete or modify list of customers (global list, testing list...)
- Stronger forms validators to add a new customer 


https://github.com/chriswilson1982/flask-mongo-app
https://github.com/punkdata/python-flask/blob/master/.circleci/config.yml
