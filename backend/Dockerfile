FROM python:3.9.7

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /backend
WORKDIR /backend/server
COPY . /backend

RUN apt-get update && \
  apt-get upgrade -y && \
  apt-get install -y \
  default-jdk -y 

RUN ls
# create content pkl
RUN python books/rec_content.py
# create tag pkl
RUN python books/rec_data.py
# create book.json
RUN python books/data.py

RUN python manage.py migrate
RUN python manage.py loaddata books/fixtures/book.json

CMD ["python3", "manage.py", "runserver", "0:8000"]

EXPOSE 8000