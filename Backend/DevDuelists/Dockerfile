FROM python:3.11 
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install --no-cache django
RUN python manage.py makemigrations
RUN python manage.py migrate
EXPOSE 8000

ENV DJANGO_SETTINGS_MODEULE = demo.settings 
ENV PYTHONUNBUFFERED=1

CMD ["python", "manage.py", "runserver", "0.0.0.8000"]