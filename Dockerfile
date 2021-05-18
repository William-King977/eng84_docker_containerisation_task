# Using Django official image
FROM python

# Optional, but a good practice
LABEL MAINTAINER = kingbigw

# Copying the project from our OS to the specified location (in container) 
COPY eng84-airport-project /usr/src/app

# Expose required port for the base image
EXPOSE 8000

# Execute run the requirements
WORKDIR /usr/src/app
RUN python -m pip install -r requirements.txt
WORKDIR /usr/src/app/app

# Make migrations, then run the application
RUN python manage.py makemigrations
RUN python manage.py migrate
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

