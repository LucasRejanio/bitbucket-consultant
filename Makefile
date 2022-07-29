# Make file to simplify script execution

SHELL := /bin/bash

up:
	docker-compose up -d --build
 
down:
	docker-compose down

api:
	docker-compose exec api python3 main.py

charts:
	docker-compose exec charts charts-cli add-user --first-name "developer" --last-name "experience" --email "developer.experience@willbank.com" --password "willbankdx@2022" --role "UserAdmin"

