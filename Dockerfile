FROM python:3.5
WORKDIR /app
ADD . .
ENV DJANGO_SETTINGS_MODULE mysite.settings
RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput
EXPOSE 8080
CMD python3 manage.py makemigrations && python3 manage.py migrate && gunicorn --bind 0.0.0.0:8080 mysite.wsgi