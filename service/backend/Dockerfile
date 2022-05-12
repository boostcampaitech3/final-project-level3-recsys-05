FROM python:3.5

RUN pip3 install django

WORKDIR /usr/src/app

COPY . .

#WORKDIR ./mytestsite
CMD ["echo","pwd"]
CMD ["python3", "manage.py", "runserver", "0:8888"]

EXPOSE 8888