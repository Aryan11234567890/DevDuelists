FROM python:3.11
WORKDIR /app
RUN pip install --no-cache-dir django 
RUN pip install djangorestframework
RUN pip install psycopg2
RUN pip install dj-database-url
RUN apt-get update && \
    apt-get install -y gcc g++
COPY . .
EXPOSE 8000
ENV DJANGO_SETTINGS_MODULE=DevDuelists.settings
ENV PYTHONUNBUFFERED=1
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]