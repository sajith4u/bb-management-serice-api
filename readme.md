## SetUp Guide

### Steps to Follow
Go to bbservice in project

1. source env/bin/activate
2. python manage.py makemigrations
3. python manage.py migrate

###  Add Initial Data
4. python manage.py initial_data

###  Start Server
5. python manage.py runserver


### How to Test BMS API

Go to postman_docs & collect the BMS API.postman_collection.json and export to postman

### Available API to Test

1. Get All Players
2. Get Player Details
3. Get All Teams
4. Get Team Details
5. Get 90th percentile players in Team
6. All Games (scoreboard)
7. Game Details


