FROM python:3.9

EXPOSE 5000

WORKDIR /app

COPY requirements.txt /app
COPY templates /app/templates

RUN pip install -r requirements.txt --upgrade pip

COPY . /app
CMD python app.py