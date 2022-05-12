FROM python:3.5

RUN pip3 install django
RUN pip3 install requests

WORKDIR /usr/src/app

COPY . .

#WORKDIR ./mytestsite
CMD ["echo","pwd"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8888"]

EXPOSE 8888