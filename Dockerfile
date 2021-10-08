FROM python:3
ENV PYTHONUNBUFFERED=1
RUN mkdir /django-recipe
WORKDIR /django-recipe
COPY requirements.txt /django-recipe/
RUN pip install -r requirements.txt
COPY . /django-recipe/ 